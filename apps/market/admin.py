from django.contrib import admin
from .models import Commodity, Comment, Classification
from django_summernote.admin import SummernoteModelAdmin

# Register your models here.

class CommodityAdmin(SummernoteModelAdmin):
    summernote_fields = ('c_detail', )

class CommentAdmin(SummernoteModelAdmin):
    summernote_fields = ('content', )

admin.site.register(Commodity, CommodityAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Classification)