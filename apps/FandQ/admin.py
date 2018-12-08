from django.contrib import admin
from .models import Notice
from django_summernote.admin import SummernoteModelAdmin
# Register your models here.
class contentnote(SummernoteModelAdmin):
    summernote_fields = ('content', )
admin.site.register(Notice, contentnote)