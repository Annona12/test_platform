# -*- coding: utf-8 -*-
# 开发者:Annona
# 开发时间:2023/11/12 17:36
# Celery的入口
# 创建celery实例
from celery import Celery

# 为celery使用django配置文件进行设置
import os
if not os.getenv('DJANGO_SETTINGS_MODULE'):
    os.environ['DJANGO_SETTINGS_MODULE'] = 'test_platform.settings.dev'

celery_app = Celery('meiduo')

# 加载配置
celery_app.config_from_object('celery_task.config')

# 注册任务
celery_app.autodiscover_tasks(['celery_task.sms','celery_task.email'])