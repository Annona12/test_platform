from django.db import models


# Create your models here.
class Area(models.Model):
    """省市区"""
    name = models.CharField(max_length=20, verbose_name='名称')
    # 自关联字段的外键指向自身，所以models.ForeignKey('self')
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, related_name='subs', null=True, blank=True,
                               verbose_name='上级行政区域id')

    class Meta:
        db_table = 'tb_areas'
        verbose_name = '省市区'
        verbose_name_plural = '省市区'

    def __str__(self):
        return self.name
