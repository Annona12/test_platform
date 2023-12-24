# -*- coding: utf-8 -*-
# 开发者:Annona
# 开发时间:2023/12/17 14:08
from django.urls import re_path
from . import views

urlpatterns = [
    # 获取登录用户需要提交的购物车列表
    re_path(r'^orders/settlement/$', views.OrderSettlementView.as_view(), name='settlement'),
    # 提交订单
    re_path(r'^orders/commit/$', views.OrderCommitView.as_view(), name='commit'),
    # 评价订单
    re_path(r'^orders/comment/$', views.OrderCommentView.as_view(), name='comment'),

]
