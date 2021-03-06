from django.db import models
from django.utils.timezone import now
from apps.account.models import User_Info
import datetime


class Classification(models.Model):
    '''商品分类数据库模型'''

    name = models.CharField(verbose_name='商品分类名称', default=None, max_length=64, blank=False, unique=True)

    create_time = models.DateTimeField(verbose_name='创建时间', default=now)

    create_man = models.ForeignKey(User_Info, verbose_name='创建人', on_delete=models.CASCADE, blank=False, default='')

    class Meta:
        ordering = ['create_time']
        verbose_name = '商品分类'
        verbose_name_plural = verbose_name
        db_table = 'Classification'

    def __str__(self):
        return self.name


class CComment(models.Model):
    '''商品评论表'''
    fromUser = models.ForeignKey(User_Info, verbose_name='来源人', on_delete=models.CASCADE)

    content = models.TextField(verbose_name='评论内容', blank=False, default="")

    update_time = models.DateTimeField(verbose_name='上传时间', default=now)

    star = models.IntegerField(verbose_name='点赞数', default=0)

    def __str__(self):
        return self.fromUser.nickname

    class Meta:
        ordering = ['-update_time']
        verbose_name = '评论'
        verbose_name_plural = '商品评论列表'
        db_table = 'CComment'
        get_latest_by = 'update_time'


class CStarRecord(models.Model):
    '''点赞记录，用于防止多次点赞'''
    comment = models.ForeignKey(CComment, on_delete=models.CASCADE)

    star_man = models.ForeignKey(User_Info, on_delete=models.CASCADE)


class CommodityImage(models.Model):
    img = models.ImageField(verbose_name='商品图片', blank=False, default='', upload_to='commodity')

    class Meta:
        verbose_name = '商品图片'
        verbose_name_plural = verbose_name + "列表"

    def __str__(self):
        return str(self.img)


class Commodity(models.Model):
    '''商品数据库模型'''
    STATUS_CHOICES = (
        ('s', '草稿'),
        ('p', '发表'),
        ('o', '已卖出')
    )

    seller = models.ForeignKey(User_Info, verbose_name='卖家', on_delete=models.CASCADE)

    detail = models.TextField(verbose_name='商品内容', default=None, blank=False)

    views = models.PositiveIntegerField(verbose_name='浏览量', default=0)

    price = models.FloatField(verbose_name='价格', default=0.0, blank=False)

    status = models.CharField(verbose_name='商品状态', max_length=10, choices=STATUS_CHOICES, default='s')

    create_time = models.DateTimeField(verbose_name='创建时间', default=now)

    last_mod_time = models.DateTimeField(verbose_name='最后修改时间', default=now)

    last_mod_date = models.DateField(verbose_name='最后编辑日期', default=now)

    classification = models.ForeignKey(Classification, verbose_name='商品分类', blank=False, null=True,
                                       on_delete=models.CASCADE)

    comment = models.ManyToManyField(CComment, verbose_name='商品评论', blank=True)

    commodity_img = models.ManyToManyField(CommodityImage, verbose_name='商品图片', default='', blank=True)

    class Meta:
        verbose_name = '商品'
        verbose_name_plural = '商品列表'
        db_table = 'Commodity'
        ordering = ['-last_mod_date', '-views']

    def __str__(self):
        return self.detail[:30]


class CommodityOrder(models.Model):
    '''商品订单'''
    STATUS_CHOICE = (
        ('未确认', '未确认'),
        ('已确认', '已确认'),
        ('已发货', '已发货'),
        ('已完成', '已完成'),
        ('已评价', '已评价'),
        ('已取消', '已取消'),
    )

    id = models.BigIntegerField(verbose_name='订单号', primary_key=True, blank=False)

    commodity = models.ForeignKey(Commodity, verbose_name='关联商品', on_delete=models.CASCADE)

    buyer = models.ForeignKey(User_Info, verbose_name='购买人', on_delete=models.CASCADE)

    address = models.CharField(verbose_name='收货地址', max_length=100, blank=True)

    create_time = models.DateTimeField(verbose_name='订单产生时间', default=now, blank=False)

    end_time = models.DateTimeField(verbose_name='订单完成时间', blank=True, default=None, null=True)

    unCompleteDeadline = models.DateTimeField(verbose_name='自动完成时间', blank=True, default=None, null=True)

    unConfirmDeadline = models.DateTimeField(verbose_name='卖家未确认自动结束订单截止时间', blank=True, default=None, null=True)

    status = models.CharField(verbose_name='订单状态', choices=STATUS_CHOICE, default='未支付', blank=False, max_length=10)

    class Meta:
        verbose_name = '商品订单'
        verbose_name_plural = verbose_name + '列表'
        db_table = 'commodityOrder'
        ordering = ['-create_time']

    def __str__(self):
        return self.commodity.detail


class BuyerRateModel(models.Model):
    '''买家评价'''

    rateChoice = (
        ('好评', '好评'),
        ('差评', '差评')
    )

    relatedOrder = models.ForeignKey(CommodityOrder, verbose_name='关联订单', on_delete=models.CASCADE, default=None,
                                     blank=False)

    content = models.TextField(verbose_name='评价内容', default=None, blank=False)

    create_time = models.DateTimeField(verbose_name='评价时间', default=now, blank=False)

    rateType = models.CharField(verbose_name='评价类型', default='好评', max_length=10, choices=rateChoice)


    class Meta:
        verbose_name = '买家评价'
        verbose_name_plural = verbose_name + '列表'
        db_table = 'BuyerRateModel'
        ordering = ['-create_time']

    def __str__(self):
        return self.relatedOrder.commodity.detail


class CommodityCollection(models.Model):
    '''用户收藏商品关联数据库模型'''

    relatedUser = models.PositiveIntegerField(verbose_name='关联用户ID', blank=False, default='')

    relatedCommodity = models.PositiveIntegerField(verbose_name='关联商品ID', blank=False, default='')

    collectionTime = models.DateTimeField(verbose_name='收藏时间', default=now, blank=False)

    class Meta:
        verbose_name = '收藏的商品'
        verbose_name_plural = verbose_name + '列表'
        db_table = 'CommodityCollection'
        ordering = ['-collectionTime']