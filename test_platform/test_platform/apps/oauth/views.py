import logging
import re

from QQLoginTool.QQtool import OAuthQQ
from django import http
from django.contrib.auth import login
from django.http import JsonResponse
from django.conf import settings
from django.views import View

# Create your views here.

# 创建日志输输出器
from django_redis import get_redis_connection

from carts.utils import merge_carts_cookies_redis
from oauth.models import OAuthQQUser
from oauth.util import generate_access_token, check_access_token
from users.models import User

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
        logger.info('生成的oauth对象为:', oauth)
        try:
            access_token = oauth.get_access_token(code)
            open_id = oauth.get_open_id(access_token)
        except Exception as e:
            logger.error(e)
            return http.HttpResponseServerError('OAuth2.0认证失败！')
        # 通过获取到的open_id对比查看数据库里面是否已经绑定
        try:
            oauth_user = OAuthQQUser.object.get(open_id)
        except OAuthQQUser.DoesNotExist as e:
            # 如果不存在，需要定位到绑定用户的页面
            # 将openid通过加密方法加密再返回给客户
            open_id_secret = generate_access_token(open_id)
            data = [{'open_id': open_id_secret}]
            return JsonResponse({'status': '200', 'msg': '重定向到绑定用户页面！', 'data': data},
                                json_dumps_params={'ensure_ascii': False})
        else:
            # 如果存在，直接登录
            login(request, oauth_user.user)
            # 将用户名写入到cookie
            # response = {}
            # request.set_cookie('username', oauth_user.user.username, max_age=3600 * 24 * 15)
            # 3、返回响应
            return JsonResponse({'status': '200', 'msg': '该用户已经绑定QQ,登录到首页！'},
                                json_dumps_params={'ensure_ascii': False})

    def post(self, request):
        # 接收参数
        mobile = request.POST.get('mobile')
        pwd = request.POST.get('password')
        sms_code_client = request.POST.get('sms_code')
        access_token = request.POST.get('access_token')
        if not all([mobile, pwd, sms_code_client, access_token]):
            return http.HttpResponseForbidden('缺少必传参数')
        # 判断手机号是否合法
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return http.HttpResponseForbidden('请输入正确的手机号码')
        # 判断密码是否合格
        if not re.match(r'^[0-9A-Za-z]{8,20}$', pwd):
            return http.HttpResponseForbidden('请输入8-20位的密码')
        # 判断验证码是否合格
        redis_conn = get_redis_connection('verify_code')
        sms_code_server = redis_conn.get('sms_%s' % mobile)
        if not sms_code_server:
            return http.HttpResponseForbidden('短信验证码已失效，请重新获取！')
        if sms_code_client != sms_code_server.decode():
            return http.HttpResponseForbidden('输入的短信验证码有无，请检查！')
        # 判断openid是否有效
        openid = check_access_token(access_token)
        if not openid:
            return http.HttpResponseForbidden('openid已失效')
        # 使用手机号码查询用户是否存在：（1）存在直接绑定user;（2）不存在需要新建用户
        try:
            user = User.objects.get(mobile=mobile)
        except User.DoesNotExist as e:
            # 如果手机号不存在新建用户
            user = User.objects.create_user(username=mobile, password=pwd, mobile=mobile)
        else:
            # 如果用户存在需要校验密码
            if not user.check_password(pwd):
                return http.HttpResponseForbidden('账号或密码错误，请检查！！！')
        try:
            oauth_user = OAuthQQUser.objects.create(user=user, openid=openid)
        except Exception as e:
            logger.error(e)
            return http.HttpResponseForbidden('服务端出错！！！')
        # openid已绑定美多商城用户:oauth_user.user表示从QQ登陆模型类对象中找到对应的用户模型类对象
        login(request, oauth_user.user)
        response = http.JsonResponse({'status': '200', 'msg': '用户已经绑定QQ完成,登录到首页！'})
        response.set_cookie('username', oauth_user.user.username, max_age=3600 * 24 * 15)
        # 用户登录成功，合并cookie购物车到redis购物车
        response = merge_carts_cookies_redis(request=request, user=user, response=response)
        return response


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
