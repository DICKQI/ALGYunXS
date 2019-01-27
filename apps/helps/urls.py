from django.urls import path
from .views.listHelps import ListHelps
from .views.helpsInfo import HelpsInfoView

app_name = 'helps'
urlpatterns = [
    path('<int:pid>/', HelpsInfoView.as_view(), name='helpsInfo'),
    path('list/', ListHelps.as_view(), name='listHelps')
]
