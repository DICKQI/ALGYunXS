from django.db import models
from apps.account.models import User_Info
from django.utils.timezone import now


class Tailwind(models.Model):
    '''顺风帮订单数据库模型'''
    STATUS_CHOICES = (
        ('u', '未支付'),
        ('p', '等待接单'),  # 已支付
        ('t', '已被接单'),
        ('c', '已完成')
    )

    TYPE_CHOICE = (
        ('代送', '代送'),
        ('代办', '代办')
    )

    initiator = models.ForeignKey(User_Info, verbose_name='委托人', on_delete=models.CASCADE)

    taskContent = models.CharField(verbose_name='任务内容', max_length=100, default='', blank=False)

    beginTime = models.DateTimeField(verbose_name='开始时间', default=now, blank=False)

    endTime = models.DateTimeField(verbose_name='截止时间', blank=False)

    serviceType = models.CharField(verbose_name='服务类型', max_length=100, choices=TYPE_CHOICE, default='代送', blank=False)

    beginPlace = models.CharField(verbose_name='开始地点', default='', max_length=100, blank=False)

    endPlace = models.CharField(verbose_name='结束地点', default='', max_length=100, blank=True) # 代办任务的时候，结束地点可为空

    status = models.CharField(verbose_name='状态', choices=STATUS_CHOICES, max_length=100, default='u', blank=False)

    money = models.FloatField(verbose_name='金额', blank=False, default=0.0)

    class Meta:
        verbose_name = '顺风帮'
        verbose_name_plural = verbose_name + '列表'
        db_table = 'tailwind'
        ordering = ['-beginTime']


class TailwindOrder(models.Model):
    '''顺风帮受托单'''
    STATUS_CHOICES = (
        ('u', '未完成'),
        ('c', '已完成')
    )

    mandatory = models.ForeignKey(User_Info, verbose_name='受委托人', on_delete=models.CASCADE)

    tailwind = models.ForeignKey(Tailwind, verbose_name='关联顺风帮订单', on_delete=models.CASCADE)

    status = models.CharField(verbose_name='订单状态', choices=STATUS_CHOICES, max_length=100, blank=False, default='u')

    create_time = models.DateTimeField(verbose_name='创建时间', default=now, blank=False)

    end_time = models.DateTimeField(verbose_name='结束时间', blank=True)

    class Meta:
        verbose_name = '顺风帮订单'
        verbose_name_plural = verbose_name + '列表'
        db_table = 'tailwindOrder'
        ordering = ['-create_time']
