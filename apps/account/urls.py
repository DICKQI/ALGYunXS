from django.urls import path
from .views.register import RegisterView
from .views.login import LoginViews
from .views.send_email import SendView
from .views.active_user import ActiveView
from .views.userInfo import UserDashBoardView
from .views.reset_password import ResetView
app_name='account'
urlpatterns = [
    path('dashboard/', UserDashBoardView.as_view(), name='my_dashboard'),
    path('register/', RegisterView.as_view(), name='my_register'),
    path('login/', LoginViews.as_view(), name='my_login'),
    path('send_email/<str:send_type>/', SendView.as_view(), name='my__send_email'),
    path('active_user/<str:a_code>/', ActiveView.as_view(), name='my__active_user'),
    path('reset_password/<str:r_code>/', ResetView.as_view(), name='my__reset_password'),
]