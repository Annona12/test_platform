import re

from django import http
from django.contrib.auth import authenticate, login, logout
from django.http import  JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View
from django.db import DatabaseError
from django_redis import get_redis_connection

from users.models import User


class UserLoginView(View):
    """
    实现用户登录
    :param request: 请求对象
    :return: 登录结果
    """

    def get(self, request):
        return JsonResponse({'status': '200', 'msg': '接口测试通过'}, json_dumps_params={'ensure_ascii': False})

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        remembered = request.POST.get('remembered')

        if not all([username, password, remembered]):
            return http.HttpResponseForbidden('缺少必传参数')

        # 判断用户名是否是5-20个字符
        if not re.match(r'^[a-zA-Z0-9_-]{5,20}$', username):
            return http.HttpResponseForbidden('请输入5-20个字符的用户名')
        # 判断密码是否是8-20个数字
        if not re.match(r'^[0-9A-Za-z]{8,20}$', password):
            return http.HttpResponseForbidden('请输入8-20位的密码')
        # 认证登录用户
        user = authenticate(username=username, password=password)
        if user is None:
            return JsonResponse({'status': '403', 'msg': '用户名或密码错误！'}, json_dumps_params={'ensure_ascii': False})
        # 保持登录状态
        login(request, user)
        # 设置状态保持的周期
        if remembered != True:
            # 没有记住用户：浏览器会话结束就过期
            request.session.set_expiry(0)
        else:
            # 记住用户:None表示两周后过期
            request.session.set_expiry(None)
        return JsonResponse({'status': '200', 'msg': '登录成功！'}, json_dumps_params={'ensure_ascii': False})


"""感觉这个类使用起来还会有问题不完整"""


class UserLogoutView(View):
    def get(self, request):
        try:
            logout(request)
        except Exception as e:
            return JsonResponse({'status': '500', 'msg': f'退出登录失败!{{e}}'}, json_dumps_params={'ensure_ascii': False})
        else:
            return JsonResponse({'status': '200', 'msg': '退出登录成功!'}, json_dumps_params={'ensure_ascii': False})


"""感觉这个类使用起来还会有问题不完整"""


class UserInfoView(View):
    def get(self, request):
        username = request.GET.get('username')
        user = User.objects.get(username=username)
        print(user.is_authenticated)
        if user.is_authenticated:
            return JsonResponse({'status': '200', 'msg': '用户登录！', 'isLogon': True},
                                json_dumps_params={'ensure_ascii': False})
        else:
            return JsonResponse({'status': '404', 'msg': '未登录用户，请登录！', 'isLogon': False},
                                json_dumps_params={'ensure_ascii': False})


class UserRegisterView(View):
    """用户注册模块"""

    def get(self, request):
        return JsonResponse('接口测试通过')

    def post(self, request):
        """
        实现用户注册
        :param request: 请求对象
        :return: 注册结果
        """
        # 接收参数：表单参数
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        mobile = request.POST.get('mobile')
        allow = request.POST.get('allow')
        # 校验参数：前后端的校验需要分开，避免恶意用户越过前端逻辑发请求，要保证后端的安全，前后端的校验逻辑相同
        # 判断参数是否齐全:all([列表])：会去校验列表中的元素是否为空，只要有一个为空，返回false
        if not all([username, password, password2,mobile,allow]):
            return http.HttpResponseForbidden('缺少必传参数')

        # 判断用户名是否是5-20个字符
        if not re.match(r'^[a-zA-Z0-9_-]{5,20}$', username):
            return http.HttpResponseForbidden('请输入5-20个字符的用户名')
        # 判断密码是否是8-20个数字
        if not re.match(r'^[0-9A-Za-z]{8,20}$', password):
            return http.HttpResponseForbidden('请输入8-20位的密码')
        # 判断两次密码是否一致
        if password != password2:
            return http.HttpResponseForbidden('两次输入的密码不一致')
        # 判断手机号是否合法
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return http.HttpResponseForbidden('请输入正确的手机号码')
        # 判断是否勾选用户协议
        if allow != 'on':
            return http.HttpResponseForbidden('请勾选用户协议')
        # 保存注册数据：是注册业务的核心
        try:
            user = User.objects.create_user(username=username, password=password, mobile=mobile)
        except DatabaseError as e:
            return JsonResponse({'status': '500', 'msg': '注册失败！'},
                                json_dumps_params={'ensure_ascii': False})
        else:
            login(request,user)
            return JsonResponse({'status': '200', 'msg': '注册成功！'},
                                json_dumps_params={'ensure_ascii': False})

class UserUsernameCount(View):
    def get(self,request):
        try:
            username = request.GET.get('username')
            count = User.objects.filter(username=username).count()
            data = [{'count':count}]
        except Exception as e:
            return JsonResponse({'status': '500', 'msg': '查询失败！'},
                                json_dumps_params={'ensure_ascii': False})
        else:
            return JsonResponse({'status': '200', 'msg': '查询成功！','data':data},
                                json_dumps_params={'ensure_ascii': False})
    def post(self):
        pass

class UserMobileCount(View):
    def get(self,request):
        try:
            mobile = request.GET.get('mobile')
            count = User.objects.filter(mobile=mobile).count()
            data = [{'count':count}]
        except Exception as e:
            return JsonResponse({'status': '500', 'msg': '查询失败！'},
                                json_dumps_params={'ensure_ascii': False})
        else:
            return JsonResponse({'status': '200', 'msg': '查询成功！','data':data},
                                json_dumps_params={'ensure_ascii': False})
    def post(self):
        pass

class ImageCodeView(View):
    def get(self,request):
        username = request.GET.get('username')
        # 生成图形验证码
        image_code = '3D3N'
        # 保存到redis数据库
        redis_conn = get_redis_connection('verify_code')
        redis_conn.setex(username, 60, image_code)
        return JsonResponse({'status': '200', 'msg': '图形验证码设置成功！', 'data': {username:image_code}},
                            json_dumps_params={'ensure_ascii': False})


