from django.urls import path
from .views import *

app_name = 'SuperAdmin'

urlpatterns = [
    # users
    path('users/', UserStatisticsView.as_view(), name='UserStatistics'),
]