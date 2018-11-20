from django.urls import path
from .views.register import RegisterView
from .views.login import LoginViews
from .views.logout import LogoutViews
app_name='account'
urlpatterns = [
    path('register/', RegisterView.as_view(), name='my_register'),
    path('login/', LoginViews.as_view(), name='my_login'),
    path('logout/', LogoutViews.as_view(), name='my_logout'),
]