# -*- coding: utf-8 -*-
# 开发者:Annona
# 开发时间:2023/12/13 21:05
from django.urls import re_path
from . import views

urlpatterns =[
    # 购物车管理:添加购物车、查询购物车
    re_path(r'^carts/$',views.CartsView.as_view(),name='carts'),
    # 购物车管理:修改购物车
    re_path(r'^update_carts/$', views.CartsUpdate.as_view(), name='carts_update'),
    # 购物车管理:删除购物车
    re_path(r'^delete_carts/$', views.CartsDelete.as_view(), name='carts_delete'),
    # 全选gwc
    re_path(r'carts/selection/', views.CartsSelectAllView.as_view(),name='selection_all'),
    # 展示简单购物车
    re_path(r'carts/simple/', views.CartsSimpleView.as_view(),name='simple_cart'),
]