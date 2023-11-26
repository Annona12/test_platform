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

from users import constants
from users.models import User
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadData
from django.conf import settings


def check_verify_email_token(token):
    """
    反序列化，将token中的user获取
    :param token:
    :return:
    """
    s = Serializer(settings.SECRET_KEY, constants.VERIFY_EMAIL_TOKEN_EXPIRES)

    try:
        data = s.loads(token)
    except BadData as e:
        return None
    else:
        user_id = data.get('user_id')
        user_email = data.get('user_email')
        try:
            user = User.objects.get(id=user_id, email=user_email)
        except User.DoseNotExists as e:
            return None
        else:
            return user
    pass


def generate_verify_email_url(user):
    """
    生成邮箱激活链接
    :param user: 当前登录用户
    :return: http://www.meiduo.site:8000/emails/verification/?token=eyJhbGciOiJIUzUxMiIsImlhdCI6MTU1ODA2MDE0MSwiZXhwIjoxNTU4MTQ2NTQxfQ.eyJ1c2VyX2lkIjoxLCJlbWFpbCI6InpoYW5namllc2hhcnBAMTYzLmNvbSJ9.y1jaafj2Mce-LDJuNjkTkVbichoq5QkfquIAhmS_Vkj6m-FLOwBxmLTKkGG0Up4eGGfkhKuI11Lti0n3G9XI3Q
    """
    s = Serializer(settings.SECRET_KEY, constants.VERIFY_EMAIL_TOKEN_EXPIRES)
    data = {'user_id': user.id, 'user_email': user.email}
    token = s.dumps(data).decode()
    return settings.EMAIL_VERIFY_URL + '?token=' + token


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
    def authenticate(self, request, username=None, password=None, **kwargs):
        # 根据传入的username，获取用户对象，username可以是手机号也可以是用户名
        user = get_user_by_account(username)
        if user and user.check_password(password):
            return user
