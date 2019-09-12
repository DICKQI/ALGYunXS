from django.urls import path
from .views import *

app_name = 'AutoExecution'

urlpatterns = [
    path('commodity/order/', AutoOrderView.as_view(), name='autoOrderCheck'),
    path('IP/', IPInfoView.as_view(), name='IPInfo'),
]