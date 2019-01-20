from django.contrib import admin
from .models import PTJInfo
from django_summernote.admin import SummernoteModelAdmin
# Register your models here.
class PTJAdmin(SummernoteModelAdmin):
    summernote_fields = ('content', )
    list_per_page = 20
    list_display = ['publisher', 'title', 'status', 'create_time', 'last_mod_time']
    list_filter = ['status']

admin.site.register(PTJInfo, PTJAdmin)