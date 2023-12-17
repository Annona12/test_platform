import base64
import pickle

from django import http
from django.shortcuts import render

# Create your views here.
from django.views import View
from django_redis import get_redis_connection

from goods.models import SKU


class CartsSelectAllView(View):
    """全选购物车"""

    def get(self, request):
        # 接收参数
        selected = request.GET.get('selected')

        # 判断用户是否登录
        user = request.user
        if user.is_authenticated:
            # 用户已登录，操作redis购物车
            redis_conn = get_redis_connection('carts')
            # 获取所有的记录 {b'3': b'1', b'5': b'2'}
            redis_cart = redis_conn.hgetall('carts_%s' % user.id)
            # 获取字典中所有的key [b'3', b'5']
            redis_sku_ids = redis_cart.keys()
            # 判断用户是否全选
            if selected:
                # 全选
                redis_conn.sadd('selected_%s' % user.id, *redis_sku_ids)
            else:
                # 取消全选
                redis_conn.srem('selected_%s' % user.id, *redis_sku_ids)

            # 响应结果
            return http.JsonResponse({'code': '200', 'errmsg': 'OK'})
        else:
            # 用户未登录，操作cookie购物车
            # 获取cookie中的购物车数据，并且判断是否有购物车数据
            cart_str = request.COOKIES.get('carts')

            # 构造响应对象
            response = http.JsonResponse({'code': '200', 'errmsg': 'OK'})

            if cart_str:
                # 将 cart_str转成bytes类型的字符串
                cart_str_bytes = cart_str.encode()
                # 将cart_str_bytes转成bytes类型的字典
                cart_dict_bytes = base64.b64decode(cart_str_bytes)
                # 将cart_dict_bytes转成真正的字典
                cart_dict = pickle.loads(cart_dict_bytes)

                # 遍历所有的购物车记录
                for sku_id in cart_dict:
                    cart_dict[sku_id]['selected'] = selected  # True / False

                # 将cart_dict转成bytes类型的字典
                cart_dict_bytes = pickle.dumps(cart_dict)
                # 将cart_dict_bytes转成bytes类型的字符串
                cart_str_bytes = base64.b64encode(cart_dict_bytes)
                # 将cart_str_bytes转成字符串
                cookie_cart_str = cart_str_bytes.decode()

                # 重写将购物车数据写入到cookie
                response.set_cookie('carts', cookie_cart_str)

            return response


class CartsView(View):
    def post(self, request):
        """
        添加购物车
        :param request:
        :return:
        """
        # 获取参数
        sku_id = request.POST.get('sku_id')
        count = request.POST.get('count')
        selected = request.POST.get('selected')
        if not all([sku_id, count, selected]):
            return http.HttpResponseForbidden('缺少必传参数')
        # 分别判断三个值传入的是否对
        # sku_id 查看商品是否存在
        try:
            SKU.objects.get(id=sku_id)
        except SKU.DoesNotExist as e:
            return http.HttpResponseForbidden('商品不存在')
        # 判断count是否为数字
        try:
            count = int(count)
        except Exception as e:
            return http.HttpResponseForbidden('参数count有误')
        # # 判断selected是否是bool值
        # if selected:
        #     print('selected:',selected)
        #     hah = isinstance(selected, bool)
        #     print('type:',type(selected))
        #
        #     if not isinstance(selected, bool):
        #         return http.HttpResponseForbidden('参数selected有误')
        user = request.user
        # 1、如果用户登录了，则将数据存入到redis
        if user.is_authenticated:
            redis_conn = get_redis_connection('carts')
            pl = redis_conn.pipeline()
            # 新增购物车数据
            pl.hincrby('carts_%s' % user.id, sku_id, count)
            # 新增选中状态
            if selected:
                pl.sadd('selected_%s' % user.id, sku_id)
            # 执行管道
            pl.execute()
            return http.JsonResponse({'code': '200', 'errmsg': '添加购物车成功！'})
        # 2、如果用户没有登录，则将购物车数据存入到cookie
        else:
            cart_str = request.COOKIES.get('carts')
            # 如果用户操作过cookie中存储购物车内容，则直接加入内容
            if cart_str:
                # 将cart_str转成bytes,再将bytes转成base64的bytes,最后将bytes转字典
                cart_dict = pickle.loads(base64.b64decode(cart_str.encode()))
            # 如果没有，则新增加
            else:
                cart_dict = {}
            # 判断要加入购物车的商品在购物车中是否存在
            if sku_id in cart_dict:
                # 累加求和
                origin_count = cart_dict[sku_id]['count']
                count += origin_count
            cart_dict[sku_id] = {
                'count': count,
                'selected': selected
            }
            # 将字典转成bytes,再将bytes转成base64的bytes,最后将bytes转字符串
            cookie_cart_str = base64.b64encode(pickle.dumps(cart_dict)).decode()
            response = http.JsonResponse({'code': '200', 'errmsg': '添加购物车成功'})
            response.set_cookie('carts', cookie_cart_str)
            return response

    def get(self, request):
        user = request.user
        # 如果用户登录，从redis中获取
        if user.is_authenticated:
            redis_conn = get_redis_connection('carts')
            # 获取redis中user_id的购物车数据
            redis_cart = redis_conn.hgetall('carts_%s' % user.id)
            # 获取redis中的选中状态
            carts_selected = redis_conn.smembers('selected_%s' % user.id)
            # 将redis中的数据构造一下在返回给用户
            cart_dict = {}
            for sku_id, count in redis_cart.items():
                print('sku_id:', int(sku_id))
                cart_dict[str(int(sku_id))] = {
                    'count': int(count),
                    'selected': sku_id in carts_selected
                }

        # 如果用户没登录，从cookie中取
        else:
            # 用户未登录，查询cookies购物车
            cart_str = request.COOKIES.get('carts')
            if cart_str:
                # 将cart_str转成bytes,再将bytes转成base64的bytes,最后将bytes转字典
                cart_dict = pickle.loads(base64.b64decode(cart_str.encode()))
            else:
                cart_dict = {}
        # 构造购物车渲染数据
        sku_ids = cart_dict.keys()
        skus = SKU.objects.filter(id__in=sku_ids)
        cart_skus = []
        for sku in skus:
            cart_skus.append({
                'id': sku.id,
                'count': cart_dict[str(sku.id)]['count'],
                'selected': str(cart_dict[str(sku.id)]['selected']),  # 将True，转'True'，方便json解析
                'name': sku.name,
                'default_image_url': sku.default_image.url,
                'price': str(sku.price),  # 从Decimal('10.2')中取出'10.2'，方便json解析
                'amount': str(sku.price * cart_dict[str(sku.id)]['count'])
            })
        data = {
            'cart_skus': cart_skus
        }
        return http.JsonResponse({'code': '200', 'errmsg': 'OK', 'data': data})


class CartsUpdate(View):
    def post(self, request):
        """修改购物车"""
        sku_id = request.POST.get('sku_id')
        count = request.POST.get('count')
        selected = request.POST.get('selected')

        # 判断参数是否齐全
        if not all([sku_id, count]):
            return http.HttpResponseForbidden('缺少必传参数')
        # 判断sku_id是否存在
        try:
            sku = SKU.objects.get(id=sku_id)
        except SKU.DoesNotExist:
            return http.HttpResponseForbidden('商品sku_id不存在')
        # 判断count是否为数字
        try:
            count = int(count)
        except Exception as e:
            return http.HttpResponseForbidden('参数count有误')
        user = request.user
        # 1、如果用户登录，修改redis
        if user.is_authenticated:
            redis_conn = get_redis_connection('carts')
            pl = redis_conn.pipeline()
            pl.hset('carts_%s' % user.id, sku_id, count)
            if selected:
                # 如果是选中添加到set中
                pl.sadd('selected_%s' % user.id, sku_id)
            else:
                # 如果是不选中，不管之前的是什么嘛直接删除
                pl.srem('selected_%s' % user.id, sku_id)
            pl.execute()
            # 创建响应的信息
            data = {
                'id': sku_id,
                'count': count,
                'selected': selected,
                'name': sku.name,
                'default_image_url': sku.default_image.url,
                'price': sku.price,
                'amount': sku.price * count,
            }
            return http.JsonResponse({'code': '200', 'errmsg': '修改购物车成功', 'cart_sku': data})
        # 2、如果用户不登录，修改cookie
        else:
            # 用户未登录，修改cookie购物车
            # 获取cookie中的购物车数据，并且判断是否有购物车数据
            cart_str = request.COOKIES.get('carts')
            if cart_str:
                # 如果cookie中有数据，从中获取cart_dict
                cart_dict = pickle.loads(base64.b64decode(cart_str.encode()))
            else:
                # 如果不存在cookie数据，直接定义一个cart_dict
                cart_dict = {}
            # 通过传递的sku_id修改购物车内容
            cart_dict[sku_id] = {
                'count': count,
                'selected': selected
            }
            # 创建响应对象
            cart_sku = {
                'id': sku_id,
                'count': count,
                'selected': selected,
                'name': sku.name,
                'price': sku.price,
                'amount': sku.price * count,
                'default_image_url': sku.default_image.url
            }
            # 将cart_dict转成bytes类型的字典
            cart_dict_bytes = pickle.dumps(cart_dict)
            # 将cart_dict_bytes转换成bytes类型的字符串
            cart_str_bytes = base64.b64encode(cart_dict_bytes)
            # 将cart_str_bytes转换成字符串
            cookie_cart_str = cart_str_bytes.decode()

            # 将最新的购物车信息数据写入cookie
            response = http.JsonResponse({'code': '200', 'errmsg': 'OK', 'cart_sku': cart_sku})
            response.set_cookie('carts', cookie_cart_str)
            return response


class CartsDelete(View):
    def get(self, request):
        """删除购物车"""
        sku_id = request.GET.get('sku_id')
        # 判断sku_id是否存在
        try:
            SKU.objects.get(id=sku_id)
        except SKU.DoesNotExist:
            return http.HttpResponseForbidden('商品不存在')
        user = request.user

        if user.is_authenticated:
            # 用户已经登录，删除redis中的购物车商品数据
            redis_conn = get_redis_connection('carts')
            pl = redis_conn.pipeline()
            pl.hdel('carts_%s' % user.id, sku_id)
            pl.srem('selected_%s' % user.id, sku_id)
            pl.execute()
            return http.JsonResponse({'code': '200', 'errmsg': 'OK'})
        else:
            cart_str = request.COOKIES.get('carts')
            if cart_str:
                # 将 cart_str转成bytes类型的字符串
                cart_str_bytes = cart_str.encode()
                # 将cart_str_bytes转成bytes类型的字典
                cart_dict_bytes = base64.b64decode(cart_str_bytes)
                # 将cart_dict_bytes转成真正的字典
                cart_dict = pickle.loads(cart_dict_bytes)
            else:
                cart_dict = {}
            # 构造响应对象
            response = http.JsonResponse({'code': '200', 'errmsg': 'OK'})
            # 删除字典指定key所对应的记录
            if sku_id in cart_dict:
                del cart_dict[sku_id]  # 如果删除的key不存在，会抛出异常

                # 将cart_dict转成bytes类型的字典
                cart_dict_bytes = pickle.dumps(cart_dict)
                # 将cart_dict_bytes转成bytes类型的字符串
                cart_str_bytes = base64.b64encode(cart_dict_bytes)
                # 将cart_str_bytes转成字符串
                cookie_cart_str = cart_str_bytes.decode()

                # 写入新的cookie
                response.set_cookie('carts', cookie_cart_str)
            return response


class CartsSimpleView(View):
    """商品页面右上角购物车"""

    def get(self, request):
        # 判断用户是否登录
        user = request.user
        if user.is_authenticated:
            # 用户已登录，查询Redis购物车
            redis_conn = get_redis_connection('carts')
            redis_cart = redis_conn.hgetall('carts_%s' % user.id)
            cart_selected = redis_conn.smembers('selected_%s' % user.id)
            # 将redis中的两个数据统一格式，跟cookie中的格式一致，方便统一查询
            cart_dict = {}
            for sku_id, count in redis_cart.items():
                cart_dict[int(sku_id)] = {
                    'count': int(count),
                    'selected': sku_id in cart_selected
                }
        else:
            # 用户未登录，查询cookie购物车
            cart_str = request.COOKIES.get('carts')
            if cart_str:
                cart_dict = pickle.loads(base64.b64decode(cart_str.encode()))
            else:
                cart_dict = {}

        # 构造简单购物车JSON数据
        cart_skus = []
        sku_ids = cart_dict.keys()
        skus = SKU.objects.filter(id__in=sku_ids)
        for sku in skus:
            cart_skus.append({
                'id': sku.id,
                'name': sku.name,
                'count': cart_dict[str(sku.id)]['count'],
                'default_image_url': sku.default_image.url
            })

        # 响应json列表数据
        return http.JsonResponse({'code': '200', 'errmsg': 'OK', 'cart_skus': cart_skus})
