import base64
import pickle

from django import http
from django.shortcuts import render

# Create your views here.
from django.views import View
from django_redis import get_redis_connection

from goods.models import SKU


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
        if not all([sku_id, count]):
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
        # 判断selected是否是bool值
        if selected:
            if not isinstance(selected, bool):
                return http.HttpResponseForbidden('参数selected有误')
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
                cart_dict[int[sku_id]] = {
                    'count':int(count),
                    'selected':sku_id in carts_selected
                }

            pass
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
                'id':sku.id,
                'name':sku.name,
                'count': cart_dict.get(sku.id).get('count'),
                'selected': str(cart_dict.get(sku.id).get('selected')),  # 将True，转'True'，方便json解析
                'default_image_url':sku.default_image.url,
                'price':str(sku.price), # 从Decimal('10.2')中取出'10.2'，方便json解析
                'amount':str(sku.price * cart_dict.get(sku.id).get('count')),
            })
        data = {
            'cart_skus':cart_skus
        }
        return http.JsonResponse({'code': '200', 'errmsg': 'OK', 'data': data})


