from django.urls import path
from .views import *

app_name='account'
urlpatterns = [
    # baseInfo
    path('', BaseViews.as_view(), name='my_login'),
    path('register/', RegisterView.as_view(), name='my_register'),
    # userInfo
    path('dashboard/', UserDashBoardView.as_view(), name='my_dashboard'),
    path('dashboard/<int:uid>/', UserDashBoardView.as_view(), name='users_dashboard'),
    path('dashboard/me/', MeView.as_view(), name='myself_info'),
    path('dashboard/log/', UserLogView.as_view(), name='my_view_log'),
    path('reset_password/', ResetView.as_view(), name='check_r_code'),
    path('reset_password/<str:r_code>/', ResetView.as_view(), name='my__reset_password'),
    path('escheck/', ESCheckView.as_view(), name='es_check'),
    # roleInfo
    path('send_email/<str:send_type>/', SendView.as_view(), name='my__send_email'),
    path('active_user/<str:a_code>/', ActiveView.as_view(), name='my__active_user'),
    # notice
    path('notice/', CheckNotificationView.as_view(), name='checkNotification'),
    path('notice/get/', NotificationView.as_view(), name='notification'),
    path('notice/<int:nid>/<str:type>', NotificationView.as_view(), name='notificationInfo'),
    # commodity rate
    path('rate/<int:uid>/', RateInfoView.as_view(), name='user_rate'),
]