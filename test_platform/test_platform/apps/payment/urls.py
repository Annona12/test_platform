# -*- coding: utf-8 -*-
# 开发者:Annona
# 开发时间:2023/12/24 12:53
from django.urls import re_path
from . import views

urlpatterns = [
    # 提交订单获取支付宝支付页面
    re_path(r'^payment/$', views.PaymentView.as_view(), name='payment'),
    # 保存订单状态
    re_path(r'^payment/status/$', views.PaymentStatusView.as_view()),
]