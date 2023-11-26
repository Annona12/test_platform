# -*- coding: utf-8 -*-
# 开发者:Annona
# 开发时间:2023/11/26 16:10
from . import views
from django.urls import re_path

urlpatterns = [
    # 获取省市区信息
    re_path(r'^areas/$', views.AreaView.as_view(), name='areas'),
]
