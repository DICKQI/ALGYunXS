from django.urls import path
from .views import *

app_name = 'helps'
urlpatterns = [
    path('<int:pid>/', HelpsInfoView.as_view(), name='helpsInfo'),
    path('new/', HelpsInfoView.as_view(), name='newHelps'),
    path('list/', ListHelps.as_view(), name='listHelps')
]
