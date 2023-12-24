# 开发者：Annona
# 开发时间：2023/11/30 13:31
from django.urls import re_path
from . import views

urlpatterns = [
    # 获取商品列表
    re_path(r'^listView/$', views.ListView.as_view(), name='list_view'),
    # 热销排行
    re_path(r'^hot/$', views.HotGoodsView.as_view(), name='hot_list'),
    # 商品详情信息
    re_path(r'detail/$', views.DetailView.as_view(), name='detail_goods'),
    # 统计分类商品访问量
    re_path(r'detail/visit/$', views.DetailVisitView.as_view(), name='detail_visit'),


]