# 开发者：Annona
# 开发时间：2023/11/8 9:54
# 开发者：Annona
# 开发时间：2023/10/23 16:43
from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'^imageCode/$', views.ImageCodeView.as_view(), name='imageCode'),
    re_path(r'^SMSCode/$',views.SMSCodeView.as_view(),name='SMSCode')

]
