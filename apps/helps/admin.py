from django.contrib import admin
from .models import Category, Tag, AComment, Article
from django_summernote.admin import SummernoteModelAdmin
# Register your models here.

class ArticleAdmin(SummernoteModelAdmin):
    summernote_fields = ('content', )

admin.site.register(Article, ArticleAdmin)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(AComment)
