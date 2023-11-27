import json
import logging
import re

# Create your views here.
from django import http
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views import View
from django.db import DatabaseError
from django_redis import get_redis_connection

from test_platform.utils.views import LoginRequiredJSONMixin
from celery_task.email.tasks import send_verify_email
from users.models import User, Address
from users.utils import generate_verify_email_url, check_verify_email_token

logger = logging.getLogger('django')


class AddressCreateView(LoginRequiredJSONMixin, View):

    def post(self, request):
        """

        :param request:
        :return:
        """
        # 判断是否超过了20个地址

        # 没超过获取参数、校验参数返回响应信息
        # 接收参数
        # json_dict = json.loads(request.body.decode())
        receiver = request.POST.get('receiver')
        province_id = request.POST.get('province_id')
        city_id = request.POST.get('city_id')
        district_id = request.POST.get('district_id')
        place = request.POST.get('place')
        mobile = request.POST.get('mobile')
        tel = request.POST.get('tel')
        email = request.POST.get('email')

        # 校验参数
        if not all([receiver, province_id, city_id, district_id, place, mobile]):
            return http.HttpResponseForbidden('缺少必传参数')
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return http.HttpResponseForbidden('参数mobile有误')
        if tel:
            if not re.match(r'^(0[0-9]{2,3}-)?([2-9][0-9]{6,7})+(-[0-9]{1,4})?$', tel):
                return http.HttpResponseForbidden('参数tel有误')
        if email:
            if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
                return http.HttpResponseForbidden('参数email有误')
        try:
            address = Address.objects.create(
                user=request.user,
                title = receiver,
                receiver = receiver,
                province_id = province_id,
                city_id = city_id,
                district_id = district_id,
                place = place,
                mobile = mobile,
                tel = tel,
                email = email
            )

        except Exception as e:
            logger.error(e)
            return JsonResponse({'statu': '500', 'msg': '新增地址失败'})

        # 构造新增地址字典数据
        address_dict = {
            "id": address.id,
            "title": address.title,
            "receiver": address.receiver,
            "province": address.province.name,
            "city": address.city.name,
            "district": address.district.name,
            "place": address.place,
            "mobile": address.mobile,
            "tel": address.tel,
            "email": address.email
        }
        return JsonResponse({'statu': '200', 'msg': '新增加地址成功', 'data': [address_dict]})


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


"""UserLogoutView,感觉这个类使用起来还会有问题不完整"""


class UserLogoutView(View):
    def get(self, request):
        try:
            logout(request)
        except Exception as e:
            return JsonResponse({'status': '500', 'msg': f'退出登录失败!{{e}}'}, json_dumps_params={'ensure_ascii': False})
        else:
            return JsonResponse({'status': '200', 'msg': '退出登录成功!'}, json_dumps_params={'ensure_ascii': False})


"""UserInfoView,感觉这个类使用起来还会有问题不完整"""


class UserInfoView(LoginRequiredMixin, View):
    """用户中心
        1、首先用户登录之后，可以通过用户登录的用户名查找用户信息；
        2、查找到用户信息之后，将用户名&联系方式返回给用户；
        3、添加邮箱；
        4、发送邮箱验证码邮件；
        5、验证邮箱；
    """

    def get(self, request):
        data = [
            {'username': request.user.username,
             'mobile': request.user.mobile,
             'email': request.user.email,
             'email_active': request.user.email_active
             }
        ]

        return JsonResponse({'status': '200', 'msg': '个人信息请求成功！', 'data': data},
                            json_dumps_params={'ensure_ascii': False})


class EmailView(LoginRequiredJSONMixin, View):

    def put(self, request):
        """
        # 前端输入邮箱，点击保存;
        # 后端收到前端的保存请求之后校验数据，保存到数据库，并响应相关信息给客户端;
        :param request:
        :return:
        """
        # 接收参数
        params_json = json.loads(request.body.decode())
        email = params_json.get('email')

        # 校验参数
        if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return http.HttpResponseForbidden('参数email有误')
        # 将用户传入的邮箱保存到用户数据库的email字段中
        try:
            request.user.email = email
            request.user.save()
        except Exception as e:
            logger.error(e)
            return JsonResponse({'status': '500', 'msg': '添加个人邮箱失败！'})
        # 发送邮箱验证邮箱
        verify_url = generate_verify_email_url(request.user)
        send_verify_email.delay(email, verify_url)
        return JsonResponse({'status': '200', 'msg': '添加个人邮箱成功！'})


class VerifyEmailView(View):
    def get(self, request):
        """
        验证邮箱的核心思想：将当前登录用户的email_active设置为1
        :param request:
        :return:
        """
        token = request.GET.get('token')
        if not token:
            return http.HttpResponseForbidden('缺少必传参数')
        user = check_verify_email_token(token)
        if not user:
            return http.HttpResponseForbidden('无效token')
        try:
            user.email_active = True
            user.save()
        except Exception as e:
            logger.error(e)
            return http.HttpResponseForbidden('邮箱激活失败！')
        return JsonResponse({'status': '200', 'msg': '邮箱激活成功！'})


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
        sms_code = request.POST.get('sms_code')
        allow = request.POST.get('allow')
        # 校验参数：前后端的校验需要分开，避免恶意用户越过前端逻辑发请求，要保证后端的安全，前后端的校验逻辑相同
        # 判断参数是否齐全:all([列表])：会去校验列表中的元素是否为空，只要有一个为空，返回false
        if not all([username, password, password2, mobile, allow, sms_code]):
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
        # 判断短信验证码是否和存储在redis中的一样
        redis_conn = get_redis_connection('verify_code')
        redis_sms_code = redis_conn.get('sms_%s' % mobile)
        # 判断短信验证码是否失效
        if redis_sms_code is None:
            return JsonResponse({'status': '404', 'msg': '短信验证码已经失效！'},
                                json_dumps_params={'ensure_ascii': False})
        redis_sms_code = redis_sms_code.decode()
        if redis_sms_code != sms_code:
            return JsonResponse({'status': '404', 'msg': '输入的短信验证码有误！'},
                                json_dumps_params={'ensure_ascii': False})
        # 判断是否勾选用户协议
        if allow != 'on':
            return http.HttpResponseForbidden('请勾选用户协议')
        # 保存注册数据：是注册业务的核心
        try:
            user = User.objects.create_user(username=username, password=password, mobile=mobile)
        except DatabaseError as e:
            logger.error(e)
            return JsonResponse({'status': '500', 'msg': '注册失败！'},
                                json_dumps_params={'ensure_ascii': False})
        else:
            login(request, user)
            return JsonResponse({'status': '200', 'msg': '注册成功！'},
                                json_dumps_params={'ensure_ascii': False})


class UserUsernameCount(View):
    def get(self, request):
        try:
            username = request.GET.get('username')
            count = User.objects.filter(username=username).count()
            data = [{'count': count}]
        except Exception as e:
            return JsonResponse({'status': '500', 'msg': '查询失败！'},
                                json_dumps_params={'ensure_ascii': False})
        else:
            return JsonResponse({'status': '200', 'msg': '查询成功！', 'data': data},
                                json_dumps_params={'ensure_ascii': False})

    def post(self):
        pass


class UserMobileCount(View):
    def get(self, request):
        try:
            mobile = request.GET.get('mobile')
            count = User.objects.filter(mobile=mobile).count()
            data = [{'count': count}]
        except Exception as e:
            return JsonResponse({'status': '500', 'msg': '查询失败！'},
                                json_dumps_params={'ensure_ascii': False})
        else:
            return JsonResponse({'status': '200', 'msg': '查询成功！', 'data': data},
                                json_dumps_params={'ensure_ascii': False})

    def post(self):
        pass
