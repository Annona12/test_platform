"""
URL configuration for test_platform project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^', include(('users.urls', 'users'), namespace='users')),
    re_path(r'^', include(('project_setting.urls', 'project_setting'), namespace='project_setting')),
    re_path(r'^', include(('verifications.urls', 'verifications'), namespace='verifications')),
    re_path(r'^', include(('oauth.urls', 'oauth'), namespace='oauth')),
    # 省市区
    re_path(r'^', include(('areas.urls', 'areas'), namespace='areas')),
    # 首页广告区
    re_path(r'^', include(('contents.urls', 'contents'), namespace='contents')),
    # 商品区
    re_path(r'^', include(('goods.urls', 'goods'), namespace='goods')),
]
