from django.db import models


# Create your models here.

class ProjectInfomation(models.Model):
    """项目信息"""
    project_name = models.CharField(max_length=255,unique=True,verbose_name='项目名称')
    # 后续需要再田间一个创建人的信息，前端自动获取登录用户信息，后端该字段关联user表的用户名为外键
    # 再加一个创建项目的时间和修改项目的时间
    project_type = models.CharField(max_length=10,verbose_name='项目类型')
    project_description = models.CharField(max_length=255,verbose_name='项目描述')
    project_status = models.BooleanField(default=False, verbose_name='项目状态')

    class Meta:
        db_table = 'tb_project_info'
        verbose_name = '项目信息表'
        verbose_name_plural = verbose_name
