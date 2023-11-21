# -*- coding: utf-8 -*-
# 开发者:Annona
# 开发时间:2023/11/16 21:39
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadData
from django.conf import settings

from oauth import constants


def check_access_token(access_token_openid):
    """
    反解、反序列化access_token_openid
    :param access_token_openid: 密文
    :return: openid:明文
    """
    # 创建序列化器对象：序列化和反序列化的对象的参数必须是一模一样的
    s = Serializer(settings.SECRET_KEY, constants.ACCESS_TOKEN_EXPIRES)
    # 反序列化openid密文
    try:
        data = s.loads(access_token_openid)
    except BadData:
        return None
    else:
        return data.get('openid')


def generate_access_token(openid):
    s = Serializer(settings.SECRET_KEY, constants.ACCESS_TOKEN_EXPIRES)
    data = {'openid': openid}
    # serializer.dumps(数据), 返回bytes类型
    token = s.dumps(data)
    return token.decode()

# generate_access_token('13870973896')

# check_accesss_token()
