# -*- coding: utf-8 -*-
# 开发者:Annona
# 开发时间:2023/11/6 20:46
# 自定义用户认证后端
"""
自定义用户认证步骤思路：
1、将用户输入的用户信息获取到，并判断一下是用户名还是手机号，返回用户信息
2、然后自定义一个用户认证类继承自原来就有的用户后端认证类，对认证方法进行重写
3、在django框架中使用这个自定义的后端认证，配置dev.py配置文件
"""
import re

from django.contrib.auth.backends import ModelBackend
from users.models import User


def get_user_by_account(account):
    try:
        if re.match('^1[3-9]\d{9}$', account):
            # 手机号登录
            user = User.objects.get(mobile=account)
        else:
            # 用户名登录
            user = User.objects.get(username=account)
    except User.DoesNotExist as e:
        return None
    return user
class UsernameMobileAuthBackend(ModelBackend):
    def authenticate(self,request,username=None,password=None,**kwargs):
        # 根据传入的username，获取用户对象，username可以是手机号也可以是用户名
        user = get_user_by_account(username)
        if user and user.check_password(password):
            return user
