from django.contrib import admin
from .models import Commodity, CComment, Classification, CommodityImage, CommodityOrder, BuyerRateModel
from django_summernote.admin import SummernoteModelAdmin

# Register your models here.

def make_published(modeladmin, request, queryset):
    queryset.update(status='p')
def make_save(modeladmin, request, queryset):
    queryset.update(status='s')
def make_sold_out(modeladmin, request, queryset):
    queryset.update(status='o')
make_save.short_description = '设置所选为草稿'
make_published.short_description = "设置所选为发表"
make_sold_out.short_description = '设置所选为已售出'
class CommodityAdmin(SummernoteModelAdmin):
    summernote_fields = ('detail', )
    list_display = ['seller', 'price', 'status', 'create_time', 'last_mod_time']
    list_per_page = 30
    list_filter = ['status']
    search_fields = ['seller']
    actions = [make_published, make_save, make_sold_out]

class CommentAdmin(SummernoteModelAdmin):
    summernote_fields = ('content', )
    list_display = ['fromUser']
class RateAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)
    # list_display = ['relatedOrder']

admin.site.register(Commodity, CommodityAdmin)
admin.site.register(CComment, CommentAdmin)
admin.site.register(BuyerRateModel, RateAdmin)
admin.site.register(Classification)
admin.site.register(CommodityImage)
admin.site.register(CommodityOrder)