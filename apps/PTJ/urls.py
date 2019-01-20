from django.urls import path
from .views.listPTJ import ListPTJ
from .views.PTJInfo import PTJInfoView
from .views.newPTJ import NewPTJView
from .views.admin.activePTJ import ActivePTJView

app_name = 'PTJ'

urlpatterns = [
    path('list/', ListPTJ.as_view(), name='list'),
    path('new/', NewPTJView.as_view(), name='new'),
    path('<int:pid>/', PTJInfoView.as_view(), name='detail'),
    path('manage/changeStatus/', ActivePTJView.as_view(), name='changeStatus'),

]