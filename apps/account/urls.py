from django.urls import path
from .views.register import RegisterView
from .views.login import LoginViews
from .views.logout import LogoutViews
from .views.send_email import SendView
from .views.active_user import ActiveView
app_name='account'
urlpatterns = [
    path('register/', RegisterView.as_view(), name='my_register'),
    path('login/', LoginViews.as_view(), name='my_login'),
    path('logout/', LogoutViews.as_view(), name='my_logout'),
    path('send_email/', SendView.as_view(), name='my__send_email'),
    path('active_user/<str:a_code>/', ActiveView.as_view(), name='my__active_user')
]