from django.urls import path
from .views.commodityInfo import CommodityView
app_name='market'
urlpatterns = [
    path('<int:cid>/', CommodityView.as_view(), name='my_commodity'),
]