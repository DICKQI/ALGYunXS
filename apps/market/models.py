from django.db import models
from django.utils.timezone import now
from apps.account.models import User_Info


class Classification(models.Model):
    '''商品分类数据库模型'''
    cid = models.BigIntegerField(verbose_name='商品分类ID', default=1, primary_key=True)

    name = models.CharField(verbose_name='商品分类名称', default=None, max_length=64, blank=False)

    create_time = models.DateTimeField(verbose_name='创建时间', default=now)

    class Meta:
        ordering = ['name']
        verbose_name = '商品分类'
        verbose_name_plural = '商品分类标签列表'
        db_table = 'Classification'

    def __str__(self):
        return self.name


class CImage(models.Model):
    '''商品图片'''
    img = models.ImageField(verbose_name='商品图片', upload_to='commodityImage', blank=True)

class Comment(models.Model):
    '''商品评论表'''
    fromUser = models.ForeignKey(User_Info, verbose_name='来源人', on_delete=models.CASCADE)

    content = models.TextField(verbose_name='评论内容', blank=False, default="")

    update_time = models.DateTimeField(verbose_name='上传时间', default=now)

    star = models.IntegerField(verbose_name='点赞数', default=0)

    def __str__(self):
        return self.fromUser.username

    class Meta:
        ordering = ['-update_time']
        verbose_name = '评论'
        verbose_name_plural = '评论列表'
        db_table = 'comment'
        get_latest_by = 'update_time'


class StarRecord(models.Model):
    '''点赞记录，用于防止多次点赞'''
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)

    star_man = models.ForeignKey(User_Info, on_delete=models.CASCADE)

# Create your models here.
class Commodity(models.Model):
    '''商品数据库模型'''
    STATUS_CHOICES = (
        ('d', '草稿'),
        ('p', '发表'),
    )

    seller = models.ForeignKey(User_Info, verbose_name='卖家', on_delete=models.CASCADE)

    name = models.CharField(verbose_name='商品名称', max_length=100, default=None, blank=False)

    views = models.PositiveIntegerField(verbose_name='浏览量', default=0)

    c_detail = models.TextField(verbose_name='商品描述详情', blank=False)

    status = models.CharField(verbose_name='商品状态', max_length=10)

    create_time = models.DateTimeField(verbose_name='创建时间', default=now)

    last_mod_time = models.DateTimeField(verbose_name='最后修改时间', default=now)

    classification = models.ForeignKey(Classification, verbose_name='商品分类', blank=True, null=True, on_delete=models.CASCADE)

    picture = models.ManyToManyField(CImage, verbose_name='商品图片', blank=True)


    def __str__(self):
        return self.seller.nickname, self.name

