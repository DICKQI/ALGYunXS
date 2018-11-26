import time
from itertools import chain
from django.db.models.fields.related import ManyToManyField, ForeignKey
from django.db.models.fields import DateTimeField
from apps.helps.models import Category
from apps.market.models import Classification
from apps.account.models import User_Info


def model_to_dict(instance, fields=None, exclude=None):
    """
    改造django.forms.models.model_to_dict()方法
    :param instance:
    :type instance: django.db.models.Model
    :param fields:  成员名称白名单（设置时将按这个名单为准，否则输出全部）
    :param exclude: 成员名称黑名单
    :return:
    为了使外键展开，ManyToMany键展开
    """
    opts = instance._meta
    data = {}
    for f in chain(opts.concrete_fields, opts.private_fields, opts.many_to_many):
        value = f.value_from_object(instance)
        if not getattr(f, 'editable', False):
            continue
        if fields and f.name not in fields:
            continue
        if exclude and f.name in exclude:
            continue
        if isinstance(f, ManyToManyField):
            if f.verbose_name == '标签':
                value = [i.name for i in value] if instance.pk else None
            elif f.verbose_name == '商品评论':
                value = [{'id': i.id, 'fromUser': i.fromUser.nickname, 'content': i.content,
                          'time': str(i.update_time)[0:10], 'star':i.star} for i in value] if instance.pk else None
            elif f.verbose_name == '文章评论':
                value = [{'id': i.id, 'fromUser': i.from_author.nickname, 'content': i.content, 'time': i.create_time}
                         for i in value] if instance.pk else None
            elif f.verbose_name == '商品图片':
                value = {'img':[i.img.path for i in value]}
        if isinstance(f, ForeignKey):
            if f.verbose_name == '分类':
                value = Category.objects.get(cid__exact=value).name
            elif f.verbose_name == '作者':
                value = User_Info.objects.get(id=value).nickname
            elif f.verbose_name == '商品分类':
                value = Classification.objects.get(cid__exact=value).name
            elif f.verbose_name == '卖家':
                value = User_Info.objects.get(id=value).nickname
            elif f.verbose_name == '来源人':
                value = User_Info.objects.get(id=value).nickname
            elif f.verbose_name == '管理员':
                value = User_Info.objects.get(id=value).nickname
        if isinstance(f, DateTimeField):
            data_time = str(value)
            year = data_time[0:4]
            month = data_time[5:7]
            day = data_time[8:10]
            hour = data_time[11:13]
            min = data_time[14:16]
            sec = data_time[17:19]
            value = year + "-" + month + "-" + day + " " + hour + ":" + min + ":" + sec
        data[f.name] = value
    return data
