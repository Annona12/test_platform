# coding=gbk

# coding=utf-8

# -*- coding: UTF-8 -*-
import ssl
ssl._create_default_https_context =ssl._create_stdlib_context # 解决Mac开发环境下，网络错误的问题
from verifications.libs.yuntongxun.CCPRestSDK import REST

# import ConfigParser

# 主帐号
accountSid = '2c94811c8b1e335b018bae22d80d1fd2';

# 主帐号Token
accountToken = '482926e40cd6438580fdefa5f347309b';

# 应用Id
appId = '2c94811c8b1e335b018bae2700b21fde';

# 请求地址，格式如下，不需要写http://
# serverIP='app.cloopen.com';
serverIP = 'sandboxapp.cloopen.com';

# 请求端口
serverPort = '8883';

# REST版本号
softVersion = '2013-12-26';


# 发送模板短信
# @param to 手机号码
# @param datas 内容数据 格式为数组 例如：{'12','34'}，如不需替换请填 ''
# @param $tempId 模板Id


class CCP(object):
    """实现发送短信验证码的单例类"""

    def __new__(cls, *args, **kwargs):
        """
        定义单例类的初始化方法
        :param args:
        :param kwargs:
        """
        # 判断是否存在类属性_instance，_instance是类CCP的唯一对象，即单例
        if not hasattr(cls, '_instance'):
            # 如果单例不存在，初始化单例
            cls._instance = super(CCP, cls).__new__(cls, *args, **kwargs)
            # 初始化REST SDK
            cls._instance.rest = REST(serverIP, serverPort, softVersion)
            cls._instance.rest.setAccount(accountSid, accountToken)
            cls._instance.rest.setAppId(appId)
        # 返回单例
        return cls._instance

    def send_template_sms(self, to, datas, tempId):
        result = self.rest.sendTemplateSMS(to, datas, tempId)
        print(result)
        if result.get('statusCode') == '000000':
            return 0
        else:
            return -1


if __name__ == '__main__':
    CCP().send_template_sms('13870973896', ['1234', 4], 1)
