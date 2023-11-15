from django.db import models

# Create your models here.
from test_platform.utils.models import BaseModel


class OAuthQQUser(BaseModel):
    # models.CASCADE：级联删除
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='用户')
    # db_index是什么
    openid = models.CharField(max_length=64, verbose_name='openid', db_index=True)

    class Meta:
        db_table = 'tb_oauth_qq'
        verbose_name = 'QQ用户数据'
        verbose_name_plural = verbose_name
