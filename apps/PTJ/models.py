from django.db import models
from apps.account.models import User_Info
from django.utils.timezone import now


# Create your models here.

class PTJTag(models.Model):
    '''兼职信息标签'''
    name = models.CharField(verbose_name='标签名', max_length=10, default='', blank=False)

    create_time = models.DateTimeField(verbose_name='创建时间', default=now)

    class Meta:
        verbose_name = '兼职信息标签'
        verbose_name_plural = verbose_name
        db_table = 'PTJTag'
        ordering = ['-create_time']

    def __str__(self):
        return self.name


class PTJInfo(models.Model):
    '''兼职信息数据库模型'''
    publisher = models.ForeignKey(User_Info, verbose_name='发布人', on_delete=models.CASCADE)

    title = models.CharField(verbose_name='标题', max_length=50, default='', blank=False)

    content = models.TextField(verbose_name='内容', default='', blank=False)

    create_time = models.DateTimeField(verbose_name='创建时间', default=now)

    last_mod_time = models.DateTimeField(verbose_name='修改时间', default=now)

    ptj_tag =models.ManyToManyField(PTJTag, verbose_name='标签', blank=True)

    class Meta:
        verbose_name = '兼职信息'
        verbose_name_plural = '兼职信息列表'
        db_table = 'PTJInfo'
        ordering = ['-last_mod_time']

    def __str__(self):
        return self.title
