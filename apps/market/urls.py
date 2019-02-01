from django.urls import path
from .views.commodityInfo import CommodityView
from .views.CImageInfo import CImgView
from .views.listCommodity import ListCommodity
from .views.manageCommodityClassification import CommodityClassificationView

app_name = 'market'
urlpatterns = [
    path('list/', ListCommodity.as_view(), name='listCommodity'),
    path('new/', CommodityView.as_view(), name='my_new'),
    path('classification/', CommodityClassificationView.as_view(), name='Classification'),
    path('<int:cid>/', CommodityView.as_view(), name='my_commodity'),
    path('<int:cid>/image/', CImgView.as_view(), name='update_img'),
    path('<int:cid>/image/<int:mid>/', CImgView.as_view(), name='delete_img'),
]
