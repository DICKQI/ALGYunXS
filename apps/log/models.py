from django.db import models
from django.utils.timezone import now
from apps.account.models import User_Info
from apps.market.models import Commodity
from apps.helps.models import Article

class LoginLog(models.Model):

    device = (
        ('android', '安卓'),
        ('apple', '苹果'),
        ('web', '网页'),
        ('weapp', '微信小程序')
    )

    '''记录用户登录信息'''
    ip = models.CharField(verbose_name='用户ip', max_length=200, blank=False, default='')

    user = models.ForeignKey(User_Info, verbose_name='关联用户', on_delete=models.CASCADE, blank=False, default='')

    login_device = models.CharField(verbose_name='登录端', blank=False, default='web', choices=device, max_length=100)

    loginTime = models.DateTimeField(verbose_name='登录时间', default=now)

    def __str__(self):
        return self.ip

class CommodityViewLog(models.Model):
    '''记录用户浏览商品'''
    ip = models.CharField(verbose_name='用户ip', max_length=200, blank=False, default='')

    user = models.ForeignKey(User_Info, verbose_name='关联用户', on_delete=models.CASCADE, blank=False, default='')

    ViewTime = models.DateTimeField(verbose_name='登录时间', default=now)

    commodity = models.ForeignKey(Commodity, verbose_name='商品', on_delete=models.CASCADE)

    def __str__(self):
        return self.ip

class HelpsViewLog(models.Model):
    '''记录用户浏览互帮互助信息'''
    ip = models.CharField(verbose_name='用户ip', max_length=200, blank=False, default='')

    user = models.ForeignKey(User_Info, verbose_name='关联用户', on_delete=models.CASCADE, blank=False, default='')

    ViewTime = models.DateTimeField(verbose_name='登录时间', default=now)

    HelpsArticle = models.ForeignKey(Article, verbose_name='文章', on_delete=models.CASCADE)

    def __str__(self):
        return self.ip


class IpVisitTime(models.Model):
    '''同一ip访问时间记录表'''
    time = models.DateTimeField(verbose_name='时间', blank=False, default=now)

    def __str__(self):
        return str(self.time)

    class Meta:
        ordering = ['-time']

class VisitLog(models.Model):
    '''ip访问记录'''
    ip = models.CharField(verbose_name='访问ip', max_length=200, blank=False, default='', unique=True)

    visit_count = models.IntegerField(verbose_name='总访问次数', blank=False, default=1)

    five_min_visit = models.IntegerField(verbose_name='5分钟内访问次数', blank=False, default=1)

    lock = models.BooleanField(verbose_name='是否封锁', blank=False, default=False)

    time = models.ManyToManyField(IpVisitTime, verbose_name='时间')

    def __str__(self):
        return self.ip


class BlackList(models.Model):
    '''黑名单ip'''
    ip = models.CharField(verbose_name='访问ip', max_length=200, blank=False, default='', unique=True)

    time = models.DateTimeField(verbose_name='时间', blank=False, default=now)

    def __str__(self):
        return self.ip
