# Create your views here.
import logging
from decimal import Decimal
from time import timezone

from django import http
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django_redis import get_redis_connection
from test_platform.utils.views import LoginRequiredMixin, LoginRequiredJSONMixin

# Create your views here.
from goods.models import SKU
from order.models import OrderInfo
from users.models import Address

logger = logging.getLogger('django')


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
        pay_method = request.POST.get('pay_method')
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
            except Exception as e:
                # 提交订单失败，回滚
                transaction.savepoint_rollback(save_id)
                logging.error(e)
                return http.JsonResponse({'code': '500', 'errmsg': '下单失败'})
                # 数据库操作成功，提交事务
            transaction.savepoint_commit(save_id)

        return JsonResponse({'code': '200', 'errmsg': '下单成功', 'order_id': 'order_id'})