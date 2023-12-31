# -*- coding: utf-8 -*-
# 开发者:Annona
# 开发时间:2023/11/12 17:47
# 定义任务
from celery_task.sms.yuntongxun.SendTemplateSMS import CCP
from celery_task.sms import constants
from celery_task.main import celery_app


# 使用装饰器装饰异步任务，保证celery识别任务
@celery_app.task(bind=True, name='send_sms_code', retry_backoff=3)
def send_sms_code(self, mobile_client, sms_code):
    """
    :param mobile_client: 手机号
    :param sms_code: 短信验证码
    :return:成功：0 、 失败：-1
    """
    try:
        send_ret = CCP().send_template_sms(mobile_client, [sms_code, constants.SMS_CODE_REDIS_EXPIRES // 60],
                                           constants.SEND_SMS_TEMPLATE_ID)
    except Exception as e:
        raise self.retry(exec=e, max_retries=3)
    return send_ret
