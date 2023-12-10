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
    # 增加地址
    re_path(r'addresses/create/$',views.AddressCreateView.as_view(),name='address_create'),
    # 查询用户地址
    re_path(r'addresses/$',views.AddressView.as_view(),name='addresses'),
    # 修改地址信息
    re_path(r'addresses/update/$',views.UpdateAddressView.as_view(),name='addresses_update'),
    # 删除地址信息
    re_path(r'addresses/delete/$',views.DeleteAddressView.as_view(),name='addresses_delete'),
    # 设置默认地址
    re_path(r'addresses/default/$',views.DefaultAddressView.as_view(),name='addresses_default'),
    # 修改地址标题
    re_path(r'addresses/updateTitle/$',views.UpdateTitleAddressView.as_view(),name='addresses_update_title'),
    # 修改用户密码
    re_path(r'addresses/changePassword/$',views.ChangePasswordView.as_view(),name='change_password'),
    # 用户商品浏览记录
    re_path(r'^browse_histories/$', views.UserBrowseHistory.as_view(),name='browse_histories'),

]
