from django.urls import path
from .views.listHelps import ListHelps
app_name='helps'
urlpatterns = [
    path('list/', ListHelps.as_view(), name='listHelps')
]