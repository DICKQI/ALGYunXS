from django.contrib import admin
from .models import Commodity, CComment, Classification, CommodityImage
from django_summernote.admin import SummernoteModelAdmin

# Register your models here.

class CommodityAdmin(SummernoteModelAdmin):
    summernote_fields = ('c_detail', )

class CommentAdmin(SummernoteModelAdmin):
    summernote_fields = ('content', )

admin.site.register(Commodity, CommodityAdmin)
admin.site.register(CComment, CommentAdmin)
admin.site.register(Classification)
admin.site.register(CommodityImage)