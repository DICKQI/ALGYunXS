from django.urls import path
from .views.noticePost import NoticeView
from .views.noticeControl import NoticeControlView

app_name = 'FandQ'
urlpatterns = [
    path('', NoticeView.as_view(), name='checkNotice'),
    path('list/', NoticeControlView.as_view(), name='NoticeControl'),
]