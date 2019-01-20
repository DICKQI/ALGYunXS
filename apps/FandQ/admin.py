from django.contrib import admin
from .models import Notice
from django_summernote.admin import SummernoteModelAdmin



class AdminFandQ(SummernoteModelAdmin):
    list_per_page = 20
    list_display = ['title', 'last_mod_time']
    search_fields = ['title']
    summernote_fields = ('content',)


admin.site.register(Notice, AdminFandQ)