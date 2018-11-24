from django.contrib import admin
from .models import PTJInfo
from django_summernote.admin import SummernoteModelAdmin
# Register your models here.
class PTJAdmin(SummernoteModelAdmin):
    summernote_fields = ('content', )

admin.site.register(PTJInfo, PTJAdmin)