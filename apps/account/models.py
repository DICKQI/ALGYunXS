from django.db import models
from django.utils.timezone import now


class School(models.Model):
    '''学校信息数据库模型'''
    name = models.CharField(verbose_name='学校名', blank=False, default='', unique=True, max_length=100)

    abbreviation = models.CharField(verbose_name='学校名缩写', blank=False, default='', max_length=100)

    user_number = models.BigIntegerField(verbose_name='学校用户数', default=0, blank=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '学校'
        verbose_name_plural = verbose_name + '列表'
        db_table = 'School'


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

    email = models.EmailField(verbose_name='邮箱', blank=False, default=None, unique=True)

    # phone_number = models.CharField(verbose_name='手机号码', max_length=20, blank=False, default=None, unique=True)

    password = models.CharField(verbose_name='密码', max_length=1000, blank=False, default=None)

    nickname = models.CharField(verbose_name='用户昵称', max_length=20, default=None, blank=False, unique=True)

    joined_date = models.DateTimeField(verbose_name='注册时间', default=now)

    '''详细信息'''

    signature = models.CharField(verbose_name='个性签名', max_length=100, default='这个人很懒，什么都没写...', blank=True)

    user_role = models.CharField(verbose_name='用户身份', max_length=6, choices=roles, default=5)

    student_id = models.CharField(verbose_name='学号', max_length=15, default=0, blank=True)

    RealName = models.CharField(verbose_name='真实姓名', max_length=100, default=None, null=True, blank=True)

    age = models.IntegerField(verbose_name='年龄', blank=True, default=1)

    head_portrait = models.ImageField(verbose_name='头像', max_length=2000, blank=True, upload_to='head_portrait')

    credit_score = models.IntegerField(verbose_name='信用分', default=500)

    from_school = models.ForeignKey(School, verbose_name='学校', on_delete=models.CASCADE, blank=True)

    '''记录信息'''
    last_login_time = models.DateTimeField(verbose_name='最后登录时间', default=now)

    TimesOfPraise = models.IntegerField(verbose_name='好评次数', default=0)

    TimesOfBadEvaluation = models.IntegerField(verbose_name='差评次数', default=0)

    TimesOfPurchase = models.IntegerField(verbose_name='购买次数', default=0)

    def __str__(self):
        return self.nickname

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


class CommentNotifications(models.Model):
    '''评论消息通知数据流模型'''

    types = {
        ('helps', '帮助文章'),
        ('market', '商品'),
        ('message', '消息')
    }

    aboutUser = models.ForeignKey(User_Info, verbose_name='被通知的用户', on_delete=models.CASCADE)

    relatedID = models.IntegerField(verbose_name='关联评论id', default=0, blank=False)

    type = models.CharField(verbose_name='消息类型', choices=types, max_length=20)

    isRead = models.BooleanField(verbose_name='是否已读', default=False, blank=False)

    noticeTime = models.DateTimeField(verbose_name='通知时间', default=now, blank=False)

    @staticmethod
    def send(id, type, user_id):
        '''发送消息'''
        user = User_Info.objects.get(id=user_id)
        CommentNotifications.objects.create(
            aboutUser=user,
            relatedID=id,
            type=type
        )

    class Meta:
        db_table = 'CommentNotifications'

    def __str__(self):
        return self.relatedID


class OrderNotification(models.Model):
    '''订单通知'''
    relatedUser = models.ForeignKey(User_Info, verbose_name='通知用户', on_delete=models.CASCADE)

    relatedCommodityID = models.BigIntegerField(verbose_name='关联的商品', default=None, null=False, blank=False)

    relatedOrderID = models.BigIntegerField(verbose_name='关联订单', default=None, null=False, blank=False)

    noticeTime = models.DateTimeField(verbose_name='通知时间', default=now)

    isRead = models.BooleanField(verbose_name='是否已读', default=False, blank=False)

    @staticmethod
    def send(user, order, commodity):
        OrderNotification.objects.create(
            relatedUser=user,
            relatedCommodityID=commodity.id,
            relatedOrderID=order.id
        )

    class Meta:
        db_table = 'OrderNotifications'
        ordering = ['-noticeTime']

    def __str__(self):
        return self.relatedUser.nickname
