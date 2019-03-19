from django.urls import path
from .views import *

app_name = 'market'
urlpatterns = [
    # list
    path('list/', ListCommodity.as_view(), name='listCommodity'),
    # info
    path('new/', CommodityView.as_view(), name='my_new'),
    path('<int:cid>/', CommodityView.as_view(), name='my_commodity'),
    # classification
    path('classification/new/', CommodityClassificationView.as_view(), name='Classification'),
    path('classification/list/', CommodityClassificationView.as_view(), name='classification_list'),
    # c image
    path('<int:cid>/image/', CImgView.as_view(), name='update_img'),
    path('<int:cid>/image/<int:mid>', CImgView.as_view(), name='delete_img'),
]
