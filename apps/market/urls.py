from django.urls import path
from .views import *

app_name = 'market'

urlpatterns = [
    # list
    path('list/', ListCommodity.as_view(), name='listCommodity'),
    # info
    path('new/', CommodityView.as_view(), name='my_new'),
    path('<int:cid>/', CommodityView.as_view(), name='my_commodity'),
    # comment
    path('<int:cid>/comment/', CommentInfoView.as_view(), name='commentInfo'),
    path('<int:cid>/comment/<int:ccid>/', CommentInfoView.as_view(), name='commentDelete'),
    # order info
    path('<int:cid>/order/', OrderView.as_view(), name='place_order'),
    path('<int:cid>/order/<int:ocid>/', OrderView.as_view(), name='orderInfo'),
    # classification
    path('classification/new/', CommodityClassificationView.as_view(), name='Classification'),
    path('classification/list/', CommodityClassificationView.as_view(), name='classification_list'),
    # c image
    path('<int:cid>/image/', CImgView.as_view(), name='update_img'),
    path('<int:cid>/image/<int:mid>', CImgView.as_view(), name='delete_img'),
]
