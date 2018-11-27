from django.contrib import admin
from .models import Category, Tag, AComment, Article
from django_summernote.admin import SummernoteModelAdmin
# Register your models here.

def make_published(modeladmin, request, queryset):
    queryset.update(status='p')
make_published.short_description = "设置所选为发表"
def make_save(modeladmin, request, queryset):
    queryset.update(status='s')
make_save.short_description = '设置所选为草稿'
class ArticleAdmin(SummernoteModelAdmin):
    summernote_fields = ('content', )
    list_display = ['author', 'title', 'status']
    actions = [make_published, make_save]
admin.site.register(Article, ArticleAdmin)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(AComment)
