# -*- coding: utf-8 -*-
# 开发者:Annona
# 开发时间:2023/12/4 11:39
from django.urls import re_path
from . import views

urlpatterns = [
    # 注册账户
    re_path(r'^index/$', views.IndexView.as_view(), name='index'),
    # 登录账户
]