# 开发者：Annona
# 开发时间：2023/10/23 16:43
from django.urls import re_path
from . import views

urlpatterns = [
    # 注册账户
    re_path(r'^register/$', views.UserRegisterView.as_view(), name='register'),
    # 登录账户
    re_path(r'^login/$', views.UserLoginView.as_view(), name='login'),
    # 登出账户
    re_path(r'^logout/$', views.UserLogoutView.as_view(), name='logout'),
    # 计算账户数量
    re_path(r'^usernameCount/$', views.UserUsernameCount.as_view(), name='usernameCount'),
    # 计算手机号码数量
    re_path(r'^mobileCount/$', views.UserMobileCount.as_view(), name='mobileCount'),
    # 获取用户中心信息
    re_path(r'userInfo/$', views.UserInfoView.as_view(), name='userInfo'),
    # 添加邮箱
    re_path(r'emailSave/$', views.EmailView.as_view(), name='emailSave'),
    # 验证邮箱
    re_path(r'emailSave/verification/$', views.VerifyEmailView.as_view(), name='emailSave'),
    # re_path(r'^imageCode/$', views.ImageCodeView.as_view(), name='imageCode')

]
