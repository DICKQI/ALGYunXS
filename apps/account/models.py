from django.db import models
from django.utils.timezone import now


# Create your models here.
class User_Info(models.Model):
    '''用户信息数据库模型'''
    roles = {
        ('515400', '总管理员'),
        ('12', 'market管理员'),
        ('123', 'helps管理员'),
        ('1234', 'PTJ管理员'),
        ('99', 'VIP用户'),
        ('4', '普通用户(已验证邮箱)'),
        ('5', '普通用户(未验证邮箱)'),
        ('6', '黑名单用户'),
    }
    '''基础信息'''

    username = models.CharField(verbose_name='用户名', max_length=20, default=None, blank=False, unique=True)

    password = models.CharField(verbose_name='密码', max_length=1000, blank=False, default=None)

    nickname = models.CharField(verbose_name='用户昵称', max_length=20, default=None, blank=False)

    email = models.EmailField(verbose_name='邮箱', blank=False, default=None, unique=True)

    joined_date = models.DateTimeField(verbose_name='注册时间', default=now)

    '''详细信息'''
    phone_number = models.CharField(verbose_name='手机号码', max_length=20, blank=False, default=None)

    user_role = models.CharField(verbose_name='用户身份', max_length=6, choices=roles, default=5)

    student_id = models.CharField(verbose_name='学号', max_length=15, default=0, blank=True)

    age = models.IntegerField(verbose_name='年龄', blank=True, default=1)

    head_portrait = models.ImageField(verbose_name='头像', upload_to='head_portrait', blank=True)

    credit_score = models.IntegerField(verbose_name='信用分', default=500)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户列表'
        ordering = ['-joined_date']
        db_table = 'User_info'


class EmailVerifyRecord(models.Model):
    '''邮箱验证码'''
    type = {
        ('active', '激活'),
        ('forget', '找回密码')
    }
    status = {
        ('used', '已使用'),
        ('not_use', '未使用')
    }
    code = models.CharField(verbose_name='验证码', unique=True, max_length=20)
    email = models.CharField(verbose_name='邮箱', max_length=50)

    send_type = models.CharField(verbose_name='验证类型', choices=type, max_length=10)
    code_status = models.CharField(verbose_name='验证码使用情况', max_length=10, choices=status, default='not_use')

    class Meta:
        verbose_name = '邮箱验证码'
        verbose_name_plural = verbose_name
        db_table = 'EmailVerifyCode'

    def __str__(self):
        return self.email + " " + self.code_status
