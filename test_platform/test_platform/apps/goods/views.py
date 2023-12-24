import logging
from datetime import datetime
from django.utils import timezone  # 处理时间的工具

from django import http
from django.http import JsonResponse

from contents.utils import get_categories
from goods.models import GoodsCategory, SKU, GoodsVisitCount
from django.views import View

# Create your views here.
from goods.utils import get_breadcrumb
from order.models import OrderGoods

logger = logging.getLogger('django')


class DetailVisitView(View):
    """统计分类商品的访问量"""

    def post(self, request):
        category_id = request.POST.get('category_id')
        if not all([category_id]):
            return http.HttpResponseForbidden('缺少必传参数')
        try:
            category = GoodsCategory.objects.get(id=category_id)
        except GoodsCategory.DoesNotExist:
            return http.HttpResponseForbidden('category_id 不存在')
        # 获取当天的日期
        t = timezone.localtime()
        # 获取当天的时间字符串
        today_str = '%d-%02d-%02d' % (t.year, t.month, t.day)
        # 将当天的时间字符串转成时间对象datetime，为了跟date字段的类型匹配 2019:05:23  2019-05-23
        today_date = datetime.strptime(today_str, '%Y-%m-%d')  # 时间字符串转时间对象；datetime.strftime() # 时间对象转时间字符串
        # 判断当天中指定的分类商品对应的记录是否存在
        try:
            # 如果存在，直接获取对象
            counts_data = GoodsVisitCount.objects.get(date=today_date, category=category)
        except GoodsVisitCount.DoesNotExist as e:
            # 如果不存在，直接创建记录对应的对象
            counts_data = GoodsVisitCount()
        try:
            counts_data.category = category
            counts_data.count += 1
            counts_data.date = today_date
            counts_data.save()
        except Exception as e:
            logger.error(e)
            return http.JsonResponse({'code': '500', 'errmsg': '服务端错误！', })
        return http.JsonResponse({'code': '200', 'errmsg': 'OK'})


class DetailView(View):
    def get(self, request):
        """获取商品详情信息"""
        sku_id = request.GET.get('sku_id')
        if not all([sku_id]):
            return http.HttpResponseForbidden('缺少必传参数')
        try:
            sku = SKU.objects.get(id=sku_id)
        except SKU.DoesNotExist as e:
            return http.HttpResponseForbidden('SKU does not exist')
        sku_dict = {
            'id': sku.id,
            'name': sku.name,
            'caption': sku.caption,
            'price': sku.price,
            'cost_price': sku.cost_price,
            'market_price': sku.market_price,
            'stock': sku.stock,
            'sales': sku.sales,
            'comments': sku.comments,
            'category_id': sku.category_id,
            'spu_id': sku.spu_id,
            'default_image_url': sku.default_image.url
        }
        return http.JsonResponse({'code': '200', 'errmsg': 'OK', 'data': sku_dict})


class HotGoodsView(View):
    """热销排行"""

    def get(self, request):
        category_id = request.GET.get('category_id')
        # 查询指定分类的SKU信息，而且必须是上架的状态，然后按照销量由高到低排序，最后切片取出前两位
        skus = SKU.objects.filter(category_id=category_id, is_launched=True).order_by('-sales')[:2]

        # 将模型列表转字典列表，构造JSON数据
        hot_skus = []
        for sku in skus:
            sku_dict = {
                'id': sku.id,
                'name': sku.name,
                'price': sku.price,
                'default_image_url': sku.default_image.url  # 记得要取出全路径
            }
            hot_skus.append(sku_dict)

        return http.JsonResponse({'code': '200', 'errmsg': 'OK', 'hot_skus': hot_skus})


class ListView(View):
    """商品列表页"""

    def get(self, request):
        """提供商品列表页"""
        # 判断category_id是否存在
        category_id = request.GET.get('category_id')
        sort = request.GET.get('sort', 'default')

        if not all([category_id]):
            return http.HttpResponseForbidden('缺少必传参数')
        try:
            category = GoodsCategory.objects.get(id=category_id)
        except  GoodsCategory.DoesNotExist:
            return http.HttpResponseForbidden('GoodsCategory does not exist')
        # 查询商品频道分类
        categories = get_categories()
        # 查询面包屑导航
        breadcrumb = get_breadcrumb(category)
        # 按照排序规则查询该分类商品SKU信息
        if sort == 'price':
            # 按照价格由低到高
            sort_field = 'price'
        elif sort == 'hot':
            # 按照销量由高到低
            sort_field = '-sales'
        else:
            # 'price'和'sales'以外的所有排序方式都归为'default'
            sort = 'default'
            sort_field = 'create_time'
        data = {
            'categories': categories,
            # 'breadcrumb': breadcrumb
        }
        return JsonResponse({'status': '200', 'msg': '查询首页信息成功！', 'data': data})


class GoodsCommentView(View):
    """订单商品评价信息"""

    def get(self, request):
        sku_id = request.GET.get('sku_id')
        # 校验参数
        if not all([sku_id]):
            return http.HttpResponseForbidden('缺少必传参数')
            # 获取被评价的订单商品信息
        order_goods_list = OrderGoods.objects.filter(sku_id=sku_id, is_commented=True).order_by('-create_time')[:30]
        # 序列化
        comment_list = []
        for order_goods in order_goods_list:
            username = order_goods.order.user.username
            comment_list.append({
                'username': username[0] + '***' + username[-1] if order_goods.is_anonymous else username,
                'comment': order_goods.comment,
                'score': order_goods.score,
            })
        return http.JsonResponse({'code': '200', 'errmsg': 'OK', 'comment_list': comment_list})
