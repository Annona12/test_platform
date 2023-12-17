# 开发者：Annona
# 开发时间：2023/11/16 16:00
from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'QQAuthLogin/$', views.QQAuthURLView.as_view(), name='QQAuthLogin'),
    re_path(r'oauth_callback/$', views.QQAuthUserView.as_view(), name='oauth_callback')

]
