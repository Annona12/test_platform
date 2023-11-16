# -*- coding: utf-8 -*-
# 开发者:Annona
# 开发时间:2023/11/16 21:39
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from django.conf import settings
import constants
def generate_access_token(openid):
    s = Serializer(settings.SECRET_KEY,constants.ACCESS_TOKEN_EXPIRES)
    # serializer.dumps(数据), 返回bytes类型
    token = s.dumps({'mobile':'13870973896'})
    print(token)
    return token.decode()

generate_access_token('openid')