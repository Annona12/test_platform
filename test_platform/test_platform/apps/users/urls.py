# 开发者：Annona
# 开发时间：2023/10/23 16:43
from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'^register/$',views.UserRegisterView.as_view(),name='register'),
    re_path(r'^login/$', views.UserLoginView.as_view(), name='login')

]