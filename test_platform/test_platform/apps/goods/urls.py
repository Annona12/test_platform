# 开发者：Annona
# 开发时间：2023/11/30 13:31
from django.urls import re_path
from . import views

urlpatterns =[
    # 获取商品列表
    re_path(r'^listView/$',views.ListView.as_view(),name='list_view'),
    # 热销排行
    re_path(r'^hot/$', views.HotGoodsView.as_view()),
]