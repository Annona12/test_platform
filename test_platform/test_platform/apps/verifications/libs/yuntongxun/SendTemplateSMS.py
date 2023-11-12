# coding=gbk

# coding=utf-8

# -*- coding: UTF-8 -*-
import ssl
ssl._create_default_https_context =ssl._create_stdlib_context # ���Mac���������£�������������
from verifications.libs.yuntongxun.CCPRestSDK import REST

# import ConfigParser

# ���ʺ�
accountSid = '2c94811c8b1e335b018bae22d80d1fd2';

# ���ʺ�Token
accountToken = '482926e40cd6438580fdefa5f347309b';

# Ӧ��Id
appId = '2c94811c8b1e335b018bae2700b21fde';

# �����ַ����ʽ���£�����Ҫдhttp://
# serverIP='app.cloopen.com';
serverIP = 'sandboxapp.cloopen.com';

# ����˿�
serverPort = '8883';

# REST�汾��
softVersion = '2013-12-26';


# ����ģ�����
# @param to �ֻ�����
# @param datas �������� ��ʽΪ���� ���磺{'12','34'}���粻���滻���� ''
# @param $tempId ģ��Id


class CCP(object):
    """ʵ�ַ��Ͷ�����֤��ĵ�����"""

    def __new__(cls, *args, **kwargs):
        """
        ���嵥����ĳ�ʼ������
        :param args:
        :param kwargs:
        """
        # �ж��Ƿ����������_instance��_instance����CCP��Ψһ���󣬼�����
        if not hasattr(cls, '_instance'):
            # ������������ڣ���ʼ������
            cls._instance = super(CCP, cls).__new__(cls, *args, **kwargs)
            # ��ʼ��REST SDK
            cls._instance.rest = REST(serverIP, serverPort, softVersion)
            cls._instance.rest.setAccount(accountSid, accountToken)
            cls._instance.rest.setAppId(appId)
        # ���ص���
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
