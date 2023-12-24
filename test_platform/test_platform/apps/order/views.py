# Create your views here.
import logging
from decimal import Decimal
from django.utils import timezone

from django import http
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django_redis import get_redis_connection
from test_platform.utils.views import LoginRequiredMixin, LoginRequiredJSONMixin

# Create your views here.
from goods.models import SKU
from order.models import OrderInfo, OrderGoods
from users.models import Address

logger = logging.getLogger('django')


class OrderCommentView(LoginRequiredJSONMixin, View):
    """订单商品评价"""

    def post(self, request):
        """评价订单商品"""
        # 接收参数
        order_id = request.POST.get('order_id')
        sku_id = request.POST.get('sku_id')
        score = request.POST.get('score')
        comment = request.POST.get('comment')
        is_anonymous = request.POST.get('is_anonymous')
        # 校验参数
        if not all([order_id, sku_id, score, comment]):
            return http.HttpResponseForbidden('缺少必传参数')
        try:
            OrderInfo.objects.filter(order_id=order_id, user=request.user,
                                     status=OrderInfo.ORDER_STATUS_ENUM['UNCOMMENT'])
        except OrderInfo.DoesNotExist:
            return http.HttpResponseForbidden('参数order_id错误')
        try:
            sku = SKU.objects.get(id=sku_id)
        except SKU.DoesNotExist:
            return http.HttpResponseForbidden('参数sku_id错误')
        if is_anonymous:
            if not isinstance(is_anonymous, bool):
                return http.HttpResponseForbidden('参数is_anonymous错误')

        # 保存订单商品评价数据
        OrderGoods.objects.filter(order_id=order_id, sku_id=sku_id, is_commented=False).update(
            comment=comment,
            score=score,
            is_anonymous=is_anonymous,
            is_commented=True
        )

        # 累计评论数据
        sku.comments += 1
        sku.save()
        sku.spu.comments += 1
        sku.spu.save()

        # 如果所有订单商品都已评价，则修改订单状态为已完成
        if OrderGoods.objects.filter(order_id=order_id, is_commented=False).count() == 0:
            OrderInfo.objects.filter(order_id=order_id).update(status=OrderInfo.ORDER_STATUS_ENUM['FINISHED'])

        return http.JsonResponse({'code': '200', 'errmsg': '评价成功'})

    def get(self, request):
        """展示商品评价页面"""
        order_id = request.GET.get('order_id')
        # 校验参数
        try:
            OrderInfo.objects.get(order_id=order_id, user=request.user)
        except OrderInfo.DoesNotExist:
            return http.HttpResponseNotFound('订单不存在')

        # 查询订单中未被评价的商品信息
        try:
            uncomment_goods = OrderGoods.objects.filter(order_id=order_id, is_commented=False)
        except Exception:
            return http.HttpResponseServerError('订单商品信息出错')
        # 构造待评价商品数据
        uncomment_goods_list = []
        for goods in uncomment_goods:
            uncomment_goods_list.append({
                'order_id': goods.order.order_id,
                'sku_id': goods.sku.id,
                'name': goods.sku.name,
                'price': str(goods.price),
                'default_image_url': goods.sku.default_image.url,
                'comment': goods.comment,
                'score': goods.score,
                'is_anonymous': str(goods.is_anonymous),
            })
        return JsonResponse({'code': '200', 'errmsg': '下单成功', 'data': uncomment_goods_list})


class OrderSettlementView(LoginRequiredJSONMixin, View):
    def get(self, request):
        """
        1、获取登录用户：
        （1）如果用户未登录提示，用户未登录信息
        （2）如果用户登录了，返回给用户购物车的信息
        :param request:
        :return:
        """
        user = request.user
        try:
            addresses = Address.objects.get(id=user.default_address_id, user=user, is_deleted=False)
        except Exception as e:
            addresses = None
        # 查询购物车中被选中的商品
        redis_conn = get_redis_connection('carts')
        # pl = redis_conn.pipeline()
        # 购物车中所有的商品,包括未勾选和已勾选的
        redis_cart = redis_conn.hgetall('carts_%s' % user.id)
        # 勾选的购物车信息
        redis_cart_selected = redis_conn.smembers('selected_%s' % user.id)
        # 将被勾选的筛选出来重新构造
        new_selected_cart = {}
        for sku_id in redis_cart_selected:
            new_selected_cart[int(sku_id)] = int(redis_cart[sku_id])
        # 获取被勾选的商品的sku_id
        sku_ids = new_selected_cart.keys()
        skus = SKU.objects.filter(id__in=sku_ids)
        total_count = 0
        total_amount = Decimal(0.00)
        # 取出所有sku
        for sku in skus:
            sku.count = new_selected_cart[sku.id]
            sku.amount = sku.price * sku.count

            # 累加数量和金额
            total_count += sku.count
            total_amount += sku.amount
        # 默认指定邮费
        freight = Decimal(10.00)
        skus_list = list(skus.values())
        data = {
            'addresses': {
                'id': addresses.id,
                'title': addresses.title,
                'receiver': addresses.receiver,
                'place': addresses.place,
                'mobile': addresses.mobile,
                'city_name': addresses.city.name,
                'district_name': addresses.district.name,
                'province_name': addresses.province.name,

            },
            'skus': skus_list,
            'total_count': total_count,
            'total_amount': total_amount,
            'freight': freight,
            'payment_amount': total_amount + freight,
        }
        return JsonResponse({'status': '200', 'msg': '查询首页信息成功！', 'data': data})


class OrderCommitView(LoginRequiredJSONMixin, View):
    """提交订单"""

    def post(self, request):
        """保存订单基本信息和订单商品信息"""
        address_id = request.POST.get('address_id')
        pay_method = int(request.POST.get('pay_method'))
        # 校验参数
        if not all([address_id, pay_method]):
            return http.HttpResponseForbidden('缺少必传参数')
            # 判断address_id是否合法
        try:
            address = Address.objects.get(id=address_id)
        except Address.DoesNotExist:
            return http.HttpResponseForbidden('参数address_id错误')
        # 判断pay_method是否合法
        if pay_method not in [OrderInfo.PAY_METHODS_ENUM['CASH'], OrderInfo.PAY_METHODS_ENUM['ALIPAY']]:
            return http.HttpResponseForbidden('参数pay_method错误')
        # 开启一次事务，如果下单成功返回客户订单编号，如果失败回滚
        with transaction.atomic():
            # 在操作数据库之前先保存后续如果需要如果的点
            save_id = transaction.savepoint()
            try:
                # 获取登录用户
                user = request.user
                # 获取订单编号：时间+user_id == '20190526165742000000001'
                order_id = timezone.localtime().strftime('%Y%m%d%H%M%S') + ('%09d' % user.id)
                # 保存订单基本信息（一）
                order = OrderInfo.objects.create(
                    order_id=order_id,
                    user=user,
                    address=address,
                    total_count=0,
                    total_amount=Decimal(0.00),
                    freight=Decimal(10.00),
                    pay_method=pay_method,
                    status=OrderInfo.ORDER_STATUS_ENUM['UNPAID'] if pay_method == OrderInfo.PAY_METHODS_ENUM[
                        'ALIPAY'] else OrderInfo.ORDER_STATUS_ENUM['UNSEND']
                )
                # 保存订单商品信息（多）
                # 查询redis购物车中被勾选的商品
                redis_conn = get_redis_connection('carts')
                # 所有购物车的数据，包含被勾选和未被勾选的
                redis_cart = redis_conn.hgetall('carts_%s' % user.id)
                # 被勾选的商品sku_id
                redis_selected = redis_conn.smembers('selected_%s' % user.id)

                # 构造购物车中被勾选的商品的数据 {b'1': b'1'}
                new_cart_dict = {}
                for sku_id in redis_selected:
                    new_cart_dict[int(sku_id)] = int(redis_cart[sku_id])
                # 获取被勾选的商品的sku_id
                sku_ids = new_cart_dict.keys()
                for sku_id in sku_ids:
                    # 每个商品都有多次下单的机会，直到库存不足
                    while True:
                        sku = SKU.objects.get(id=sku_id)
                        # 获取原始的库存和销量
                        origin_stock = sku.stock
                        origin_sales = sku.sales

                        # 获取要提交订单的商品数量
                        sku_count = new_cart_dict[sku_id]
                        # 判断商品数量是否大于库存，如果大于，响应库存不足
                        if sku_count > origin_stock:
                            transaction.savepoint_rollback(save_id)
                            return http.JsonResponse({'code': '500', 'errmsg': '库存不足'})
                        # 模拟网络延迟
                        # SKU减少库存，加销量
                        new_stock = origin_stock - sku_count
                        new_sales = origin_sales - sku_count
                        result = SKU.objects.filter(id=sku_id, stock=origin_stock).update(stock=new_stock,
                                                                                          sales=new_sales)
                        # 如果在更新数据时，原始数据变化了，返回0，表示有资源抢夺
                        if result == 0:
                            # 库存 10，要买1，但是在下单时，有资源抢夺，被买走1，剩下9个，如果库存依然满足，继续下单，直到库存不足为止
                            # return http.JsonResponse('下单失败')
                            continue
                        # spu 增加销量
                        sku.spu.sales += sku_count
                        sku.spu.save()
                        OrderGoods.objects.create(
                            order=order,
                            sku=sku,
                            count=sku_count,
                            price=sku.price,
                        )
                        # 累加订单商品的数量和总价到订单基本信息表
                        order.total_count += sku_count
                        order.total_amount += sku_count * sku.price

                        # 下单成功
                        break
                    # 再加上最后的运费
                order.total_amount += order.freight
                order.save()
            except Exception as e:
                # 提交订单失败，回滚
                transaction.savepoint_rollback(save_id)
                logging.error(e)
                return http.JsonResponse({'code': '500', 'errmsg': '下单失败'})
                # 数据库操作成功，提交事务
            transaction.savepoint_commit(save_id)
            data = {
                'order_id': order_id,
                'total_amount': order.total_amount,
                'pay_method': pay_method
            }

        return JsonResponse({'code': '200', 'errmsg': '下单成功', 'data': data})
