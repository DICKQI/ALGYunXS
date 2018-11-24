from django.urls import path
from .views.commodityInfo import CommodityView
from .views.newCommodity import NewCommodityView
app_name='market'
urlpatterns = [
    path('new/', NewCommodityView.as_view(), name='my_new'),
    path('<int:cid>/', CommodityView.as_view(), name='my_commodity'),
]