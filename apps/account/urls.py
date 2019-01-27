from django.urls import path
from .views import *

app_name='account'
urlpatterns = [
    path('', LoginViews.as_view(), name='my_login'),
    path('dashboard/', UserDashBoardView.as_view(), name='my_dashboard'),
    path('dashboard/me/', MeView.as_view(), name='myself_info'),
    path('register/', RegisterView.as_view(), name='my_register'),
    path('send_email/<str:send_type>/', SendView.as_view(), name='my__send_email'),
    path('active_user/<str:a_code>/', ActiveView.as_view(), name='my__active_user'),
    path('reset_password/<str:r_code>/', ResetView.as_view(), name='my__reset_password'),
]