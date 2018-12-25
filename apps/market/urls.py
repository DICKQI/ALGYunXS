from django.urls import path
from .views.commodityInfo import CommodityView
from .views.newCommodity import NewCommodityView
from .views.new_commodityImg import CImgView
from .views.deleteCommodityImg import DeleteImage
from .views.listCommodity import ListCommodity
app_name='market'
urlpatterns = [
    path('list/', ListCommodity.as_view(), name='listCommodity'),
    path('new/', NewCommodityView.as_view(), name='my_new'),
    path('<int:cid>/', CommodityView.as_view(), name='my_commodity'),
    path('<int:cid>/image/', CImgView.as_view(), name='update_img'),
    path('<int:cid>/image/<int:mid>/', DeleteImage.as_view(), name='delete_img'),
]