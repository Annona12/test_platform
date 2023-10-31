from django.db import models

# Create your models here.
class APITestcase(models.Model):
    """接口自动化测试用例"""
    testcase_story = models.CharField(max_length=255,unique=True,verbose_name='项目名称')
    title = models.CharField(max_length=255,unique=True,verbose_name='项目名称')
    description = models.CharField(max_length=255,unique=True,verbose_name='项目名称')
    level = models.CharField(max_length=255,unique=True,verbose_name='项目名称')
    action = models.CharField(max_length=255,unique=True,verbose_name='项目名称')
    xml_path = models.CharField(max_length=255,unique=True,verbose_name='项目名称')
    update_params = models.CharField(max_length=255,unique=True,verbose_name='项目名称')
    sql = models.CharField(max_length=255,unique=True,verbose_name='项目名称')
    reresult = models.CharField(max_length=255,unique=True,verbose_name='项目名称')
    result = models.CharField(max_length=255,unique=True,verbose_name='项目名称')
    execute = models.CharField(max_length=255,unique=True,verbose_name='项目名称')