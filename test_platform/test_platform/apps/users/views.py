import re

from django import http
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.views import View
from django.db import DatabaseError

from users.models import User


class UserLoginView(View):
    """
    实现用户登录
    :param request: 请求对象
    :return: 登录结果
    """

    def get(self, request):
        return JsonResponse({'status': '200', 'msg': '接口测试通过'},json_dumps_params={'ensure_ascii': False})

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
            return JsonResponse({'status': '403', 'msg': '用户名或密码错误！'},json_dumps_params={'ensure_ascii': False})
        # 保持登录状态
        login(request,user)
        # 设置状态保持的周期
        if remembered != True:
            # 没有记住用户：浏览器会话结束就过期
            request.session.set_expiry(0)
        else:
            # 记住用户:None表示两周后过期
            request.session.set_expiry(None)
        return JsonResponse({'status': '200', 'msg': '登录成功！'},json_dumps_params={'ensure_ascii': False})

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
        remembered = request.POST.get('remembered')
        # 校验参数：前后端的校验需要分开，避免恶意用户越过前端逻辑发请求，要保证后端的安全，前后端的校验逻辑相同
        # 判断参数是否齐全:all([列表])：会去校验列表中的元素是否为空，只要有一个为空，返回false
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
            return

        # 判断是否勾选用户协议
        if allow != 'on':
            return http.HttpResponseForbidden('请勾选用户协议')
        # 保存注册数据：是注册业务的核心
        # return render(request, 'register.html', {'register_errmsg': '注册失败'})
        try:
            user = User.objects.create_user(username=username, password=password, mobile=mobile)
        except DatabaseError:
            # return render(request, 'user/register.html', {'register_errmsg': '注册失败！'})
            return HttpResponse('注册失败！！！')

        # return redirect('index.html')
        # url = reverse('contents:index')
        # print('url:', url)
        # return redirect(reverse('contents:index'))
        return HttpResponse('注册成功！！！')
