import json
import logging

from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views import View
from collections import OrderedDict

from contents.models import ContentCategory
from goods.models import GoodsChannel

logger = logging.getLogger('django')


class IndexView(View):
    """提供首页广告分类
    查询并展示商品分类"""

    def get(self, request):
        # 定义一个有序的字典
        categories = OrderedDict()
        try:
            # 查询所有的37个频道
            channels = GoodsChannel.objects.all().order_by('group_id', 'sequence')
            for channel in channels:
                group_id = channel.group_id
                # group_id总共有11个组，所以需要判断一下
                if group_id not in categories:
                    categories[group_id] = {
                        'channels': [],
                        'sub_cats': []
                    }
                # 查询当前频道的类别,查询当前频道对应的类别是一对一的查询，
                # 以及查询，能
                cat1 = channel.category
                # 追加当前频道
                categories[group_id]['channels'].append(
                    {
                        'id': cat1.id,
                        'name': cat1.name,
                        'url': channel.url
                    }
                )
                # 构建当前类别的子类别
                for cat2 in cat1.subs.all():
                    cat2.sub_cats = []
                    for cat3 in cat2.subs.all():
                        cat2.sub_cats.append({
                            'id': cat3.id,
                            'name': cat3.name
                        })
                    categories[group_id]['sub_cats'].append({
                        'id': cat2.id,
                        'name': cat2.name,
                        'sub_cats': cat2.sub_cats
                    })
            # 广告数据
            contents = {}
            content_categories = ContentCategory.objects.all()
            for cat in content_categories:
                contents[cat.key] = []
                cat1_result = cat.content_set.filter(status=True).order_by('sequence')
                for cat1 in cat1_result:
                    # print(cat1)
                    cat1_dict = {
                        'id': cat1.id,
                        'category': cat1.category_id,
                        'title': cat1.title,
                        'url': cat1.url,
                        'image': cat1.image.name,
                        'text': cat1.text,
                        'sequence': cat1.sequence,
                        'status': cat1.status
                    }
                    contents[cat.key].append(cat1_dict)

            data = {
                'categories': categories,
                'contents': contents
            }
            return JsonResponse({'status': '200', 'msg': '查询首页信息成功！', 'data': data})
        except Exception as e:
            logger.error(e)
            return JsonResponse({'status': '500', 'msg': '查询首页信息错误！'})
