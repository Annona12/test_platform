from django.http import JsonResponse

# Create your views here.
from django.views import View
from django_redis import get_redis_connection
from django import http

from verifications import constants
from verifications.libs.captcha.captcha import captcha


class ImageCodeView(View):
    def get(self,request):
        username = request.GET.get('username')
        # 生成图形验证码
        text ,image= captcha.generate_captcha()
        # 保存到redis数据库
        redis_conn = get_redis_connection('verify_code')
        redis_conn.setex(username, constants.IMAGE_CODE_REDIS_EXPIRES, text)

        with open('image.jpg','wb') as file :
            file.write(image.getvalue())
            image.close()
        # print(image)
        # image.save("1.jpg")
        # return http.HttpResponse(image, content_type='image/jpg')
        return JsonResponse({'status': '200', 'msg': '图形验证码设置成功！'},
                            json_dumps_params={'ensure_ascii': False})
