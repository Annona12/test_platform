from django import http
from django.http import JsonResponse

from contents.utils import get_categories
from goods.models import GoodsCategory, SKU
from django.views import View

# Create your views here.
from goods.utils import get_breadcrumb


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
                'default_image_url': sku.default_image.url # 记得要取出全路径
            }
            hot_skus.append(sku_dict)

        return http.JsonResponse({'code': '200', 'errmsg': 'OK', 'hot_skus': hot_skus})

class ListView(View):
    """商品列表页"""

    def get(self, request):
        """提供商品列表页"""
        # 判断category_id是否存在
        category_id = request.GET.get('category_id')
        sort = request.GET.get('sort','default')

        if not all([category_id]):
            return http.HttpResponseForbidden('缺少必传参数')
        try:
            category = GoodsCategory.objects.get(id=category_id)
        except  GoodsCategory.DoesNotExist:
            return http.HttpResponseForbidden('GoodsCategory does not exis')
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
