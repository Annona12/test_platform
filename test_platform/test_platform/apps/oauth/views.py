import logging

from QQLoginTool.QQtool import OAuthQQ
from django import http
from django.contrib.auth import login
from django.http import JsonResponse
from django.conf import settings
from django.views import View

# Create your views here.

# 创建日志输输出器
from oauth.models import OAuthQQUser

logger = logging.getLogger('django')


class QQAuthUserView(View):
    def get(self, request):
        """
        用户处理扫完码之后的逻辑
        :return:
        """
        # 1、接受参数
        # (1)扫完码之后QQ互联会将code返回给用户
        code = request.GET.get('code')
        if not code:
            return http.HttpResponseForbidden('获取code失败')
        # (1)通过AuthorizationCode获取AccessToken
        # 创建工具对象
        oauth = OAuthQQ(client_id=settings.QQ_CLIENT_ID, client_secret=settings.QQ_CLIENT_SECRET,
                        redirect_uri=settings.QQ_REDIRECT_URI, state=next)
        try:
            access_token = oauth.get_access_token(code)
            open_id = oauth.get_open_id(access_token)
        except Exception as e:
            logger.error(e)
            return http.HttpResponseServerError('OAuth2.0认证失败！')
        # 通过获取到的open_id对比查看数据库里面是否已经绑定
        try:
            oauthuser = OAuthQQUser.object.get(open_id)
        except OAuthQQUser.DoesNotExist as e:
            # 如果不存在，需要定位到绑定用户的页面
            # 将openid通过加密方法加密再返回给客户
            return JsonResponse({'status': '200','msg':'重定向到绑定用户页面！','data':''},
                                json_dumps_params={'ensure_ascii': False})
            pass
        else:
            # 如果存在，直接登录
            login(request,oauthuser.user)
            # 将用户名写入到cookie
            request.set_cookie('username',oauthuser.user.username,max_age=3600 * 24 * 15)
            # 3、返回响应

            return JsonResponse({'status': '200','msg':'该用户已经绑定QQ,登录到首页！'},
                                json_dumps_params={'ensure_ascii': False})

    def post(self):
        pass


class QQAuthURLView(View):
    """点击QQ登录按钮，跳转到请求QQ登录二维码界面"""

    def get(self, request):
        next = request.GET.get('next')
        # 创建工具对象
        # oauth = OAuthQQ(client_id='appid', client_secret='appkey', redirect_uri='callback', state='')
        oauth = OAuthQQ(client_id=settings.QQ_CLIENT_ID, client_secret=settings.QQ_CLIENT_SECRET,
                        redirect_uri=settings.QQ_REDIRECT_URI, state=next)
        # 获取QQ登录扫码页面
        login_url = oauth.get_qq_url()
        data = [{'login_url': login_url}]
        # return redirect(login_url)
        return JsonResponse({'status': '200', 'data': data},
                            json_dumps_params={'ensure_ascii': False})
        pass

    def post(self):
        pass
