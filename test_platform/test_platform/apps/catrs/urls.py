# -*- coding: utf-8 -*-
# 开发者:Annona
# 开发时间:2023/12/13 21:05
from django.urls import re_path
from . import views

urlpatterns =[
    # 购物车管理
    re_path(r'^carts/$',views.CartsView.as_view(),name='carts')
]