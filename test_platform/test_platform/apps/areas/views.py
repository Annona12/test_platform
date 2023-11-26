# Create your views here.
from django import http
from django.core.cache import cache
from django.views import View
import logging
from django.http import JsonResponse

from areas.models import Area

logger = logging.getLogger('django')


class AreaView(View):
    def get(self, request):
        """
        1、发送请求之后返回省市区的信息
        :return:
        """
        area_id = request.GET.get('area_id')
        if not area_id:
            # 获取并判断是否有缓存
            province_list = cache.get('province_list')
            if not province_list:
                try:
                    province_model_list = Area.objects.filter(parent__isnull=True)
                    province_list = []
                    for province_model in province_model_list:
                        province_dict = {
                            'id': province_model.id,
                            'name': province_model.name
                        }
                        province_list.append(province_dict)
                    # 缓存省份字典列表数据:默认存储到别名为"default"的配置中
                    cache.set('province_list', province_list, 3600)

                except Exception as e:
                    logger.eror(e)
                    return JsonResponse({'status': '500', 'msg': '获取省份信息失败功！', })
            # 获取省份信息并返回
            return JsonResponse({'status': '200', 'msg': '获取省份信息成功！', 'province_list': province_list})
        else:
            # 判断是否有缓存
            sub_data = cache.get('sub_area_' + area_id)
            if not sub_data:
                try:
                    province_model = Area.objects.get(id=area_id)
                    # subs_model_list = province_model.area_set.all()
                    subs_model_list = province_model.subs.all()
                    subs = []
                    for subs_model in subs_model_list:
                        subs_model_dict = {
                            'id': subs_model.id,
                            'name': subs_model.name
                        }
                        subs.append(subs_model_dict)
                    sub_data = {
                        'id': province_model.id,
                        'name': province_model.name,
                        'subs': subs
                    }
                    # 缓存城市或者区县
                    cache.set('sub_area_' + area_id, sub_data, 3600)
                except Exception as e:
                    logger.eror(e)
                    return JsonResponse({'status': '500', 'msg': '获取市、区信息失败功！', })
            return JsonResponse({'status': '200', 'msg': '获取市、区信息成功！', 'sub_data': sub_data})
