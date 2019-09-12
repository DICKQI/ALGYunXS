from django.urls import path
from .views import *

app_name = 'FandQ'
urlpatterns = [
    path('', NoticeView.as_view(), name='checkNotice'),
    path('list/', NoticeControlView.as_view(), name='NoticeControl'),
]