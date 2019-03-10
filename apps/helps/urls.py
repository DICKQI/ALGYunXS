from django.urls import path
from .views import *

app_name = 'helps'
urlpatterns = [
    # article info
    path('<int:pid>/', HelpsInfoView.as_view(), name='helpsInfo'),
    path('new/', HelpsInfoView.as_view(), name='newHelps'),
    # star info
    path('<int:aid>/star/', StarInfoView.as_view(), name='starArticle'),
    # comment
    path('<int:aid>/comment/', CommentInfoView.as_view(), name='CommentInfo'),
    path('<int:aid>/comment/delete/<int:cid>/', CommentInfoView.as_view(), name='deleteComment'),
    # image info
    path('image/<int:aid>/', ImageView.as_view(), name='imageInfo'),
    # list info
    path('list/', ListHelps.as_view(), name='listHelps')
]
