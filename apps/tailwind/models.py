from django.db import models
from apps.account.models import User_Info
from django.utils.timezone import now


class Tailwind(models.Model):
    '''有闲订单数据库模型'''
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

    taskContent = models.TextField(verbose_name='任务内容', default='', blank=False)

    beginTime = models.DateTimeField(verbose_name='开始时间', default=now, blank=False)

    endTime = models.DateTimeField(verbose_name='截止时间', blank=False)

    serviceType = models.CharField(verbose_name='服务类型', max_length=100, choices=TYPE_CHOICE, default='代送', blank=False)

    beginPlace = models.CharField(verbose_name='开始地点', default='', max_length=100, blank=False)

    endPlace = models.CharField(verbose_name='结束地点', default='', max_length=100, blank=True) # 代办任务的时候，结束地点可为空

    status = models.CharField(verbose_name='状态', choices=STATUS_CHOICES, max_length=100, default='u', blank=False)

    money = models.FloatField(verbose_name='金额', blank=False, default=0.0)

    class Meta:
        verbose_name = '有闲'
        verbose_name_plural = verbose_name + '列表'
        db_table = 'tailwind'
        ordering = ['-beginTime']

    def __str__(self):
        return self.initiator


class TailwindOrder(models.Model):
    '''有闲受托单'''
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
        verbose_name = '有闲订单'
        verbose_name_plural = verbose_name + '列表'
        db_table = 'tailwindOrder'
        ordering = ['-create_time']

    def __str__(self):
        return self.mandatory

class TailwindUserConfig(models.Model):
    '''有闲用户个人设置'''

    relatedUser = models.OneToOneField(User_Info, verbose_name='关联主用户', on_delete=models.CASCADE, unique=True)

    dormitory = models.CharField(verbose_name='宿舍楼', default=None, null=True, blank=True, max_length=100)

    commonAcademicBuilding = models.TextField(verbose_name='常用教学楼', default=[], null=True, blank=True)


    class Meta:
        verbose_name = '有闲个人偏好设置',
        verbose_name_plural = '有闲个人设置'
        db_table = 'tailwind_config'

    def __str__(self):
        return self.relatedUser.nickname