from django.db import models
from django.utils.timezone import now
from apps.account.models import User_Info


# Create your models here.
class Category(models.Model):
    '''分类数据库模型'''
    cid = models.BigIntegerField(verbose_name='分类id', primary_key=True, default=1)

    name = models.CharField(verbose_name='分类名', default='', blank=False, max_length=10, unique=True)

    create_time = models.DateTimeField(verbose_name='创建时间', default=now)

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = '分类列表'
        db_table = 'Category'
        ordering = ['-create_time']

    def __str__(self):
        return self.name


class Tag(models.Model):
    '''标签数据库模型'''
    name = models.CharField(verbose_name='标签名', max_length=10, default='', blank=False)

    create_time = models.DateTimeField(verbose_name='创建时间', default=now)

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = '标签列表'
        db_table = 'Tag'
        ordering = ['-create_time']

    def __str__(self):
        return self.name


class AComment(models.Model):
    '''评论数据库模型'''
    from_author = models.ForeignKey(User_Info, verbose_name='来源人', on_delete=models.CASCADE, blank=False)

    content = models.TextField(verbose_name='评论内容', blank=False, default='')

    create_time = models.DateTimeField(verbose_name='创建时间', default=now)

    star = models.IntegerField(verbose_name='点赞数', default=0)

    class Meta:
        verbose_name = '文章评论'
        verbose_name_plural = verbose_name
        db_table = 'AComment'
        ordering = ['-create_time']

    def __str__(self):
        return self.from_author.nickname


class AStarRecord(models.Model):
    '''防止重复点赞'''
    comment = models.ForeignKey(AComment, verbose_name='被点赞的评论', on_delete=models.CASCADE)

    star_man = models.ForeignKey(User_Info, verbose_name='点赞人', on_delete=models.CASCADE)


class Article(models.Model):
    '''文章数据库模型'''
    STATUS_CHOICES = (
        ('s', '草稿'),
        ('p', '发表'),
    )

    author = models.ForeignKey(User_Info, verbose_name='作者', on_delete=models.CASCADE, blank=False)

    title = models.CharField(verbose_name='标题', default='', blank=False, max_length=30)

    content = models.TextField(verbose_name='内容', blank=False, default='')

    status = models.CharField(verbose_name='文章状态', choices=STATUS_CHOICES, max_length=2, default='草稿')

    views = models.IntegerField(verbose_name='浏览量', default=0)

    create_time = models.DateTimeField(verbose_name='创建时间', default=now)

    last_mod_time = models.DateTimeField(verbose_name='最后修改时间', default=now)

    tags = models.ManyToManyField(Tag, verbose_name='标签', blank=True)

    category = models.ForeignKey(Category, verbose_name='分类', blank=False, on_delete=models.CASCADE)

    comment = models.ManyToManyField(AComment, verbose_name='文章评论', blank=True)

    stars = models.IntegerField(verbose_name='点赞数', blank=False, default=0)

    img = models.ImageField(verbose_name='文章附图', default='', blank=True, upload_to='article')

    class Meta:
        verbose_name = '互帮互助文章'
        verbose_name_plural = '文章列表'
        db_table = 'Article'
        ordering = ['-last_mod_time']

    def __str__(self):
        return self.title


class HelpsStarRecord(models.Model):
    '''防止给文章重复点赞（点赞记录）'''
    article = models.ForeignKey(Article, verbose_name='被点赞的文章', on_delete=models.CASCADE)

    star_man = models.ForeignKey(User_Info, verbose_name='点赞人', on_delete=models.CASCADE)