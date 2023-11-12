import logging
import random


# Create your views here.
from django.views import View
from django_redis import get_redis_connection
from django import http
from django.http import JsonResponse

from verifications import constants
from verifications.libs.captcha.captcha import captcha
from celery_task.sms.tasks import send_sms_code
from verifications.libs.yuntongxun.SendTemplateSMS import CCP


# 创建日志输出器
logger = logging.getLogger('django')
class SMSCodeView(View):
    """短信验证码"""

    def get(self, request):
        # 1、接收并提取参数
        mobile_client = request.GET.get('mobile')
        username_client = request.GET.get('username')
        image_code_client = request.GET.get('image_code')
        # 2、校验必传参数，校验通过发送短信验证码
        if not all([mobile_client, username_client, image_code_client]):
            return http.HttpResponseForbidden('缺少必传参数！！！')
        redis_conn = get_redis_connection('verify_code')
        send_flag = redis_conn.get('send_flag_%s' % mobile_client)
        if send_flag:
            return JsonResponse({'status': '404', 'msg': '发送验证码过于频繁！'},
                                json_dumps_params={'ensure_ascii': False})
        # 获取redis中的图形验证码
        redis_image_code = redis_conn.get('image_%s' % username_client)
        if redis_image_code is None:
            return JsonResponse({'status': '404', 'msg': '图形验证码已经失效！'},
                                json_dumps_params={'ensure_ascii': False})
        # 删除验证码防止恶意测试
        redis_conn.delete(username_client)
        # redis提取出来的数据类型是bytes,需要转换成字符串
        redis_image_code = redis_image_code.decode()
        # 用户体验提升，验证码不区分大小写
        if redis_image_code.lower() != image_code_client.lower():
            # 图形验证码校验失败
            return JsonResponse({'status': '404', 'msg': '图形验证码校验失败！'},
                                json_dumps_params={'ensure_ascii': False})
        # ①图形验证码校验通过：生成短信验证码，并保存验证码到redis中，发送验证码
        # sms_code = random.randint(1000,9999)
        # 生成随机的4位数字，如果不足4位前面补0，0008
        sms_code = '%04d' % random.randint(0, 9999)
        logger.info(sms_code)
        # 将短信验证码存储在redis中
        redis_conn.setex('sms_%s' % mobile_client, constants.SMS_CODE_REDIS_EXPIRES, sms_code)
        redis_conn.setex('send_flag_%s' % mobile_client,constants.SEND_SMS_CODE_INTERVAL,1)
        # 发送短信验证码
        pl = redis_conn.pipeline()
        pl.setex('sms_%s' % mobile_client, constants.SMS_CODE_REDIS_EXPIRES, sms_code)
        pl.setex('send_flag_%s' % mobile_client, constants.SEND_SMS_CODE_INTERVAL, 1)
        pl.execute()
        send_sms_code.delay(mobile_client,sms_code)
        # CCP().send_template_sms(mobile_client, [sms_code, constants.SMS_CODE_REDIS_EXPIRES // 60],
        #                         constants.SEND_SMS_TEMPLATE_ID)
        # 3、返回响应结果
        return JsonResponse({'status': '200', 'msg': '发送短信验证码成功！'},
                            json_dumps_params={'ensure_ascii': False})
        pass


class ImageCodeView(View):
    def get(self, request):
        username = request.GET.get('username')
        # 生成图形验证码
        text, image = captcha.generate_captcha()
        # 保存到redis数据库
        redis_conn = get_redis_connection('verify_code')
        redis_conn.setex('image_%s' % username, constants.IMAGE_CODE_REDIS_EXPIRES, text)

        with open('image.jpg', 'wb') as file:
            file.write(image.getvalue())
            image.close()
        # print(image)
        # image.save("1.jpg")
        # return http.HttpResponse(image, content_type='image/jpg')
        return JsonResponse({'status': '200', 'msg': '图形验证码设置成功！'},
                            json_dumps_params={'ensure_ascii': False})
