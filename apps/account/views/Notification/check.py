from apps.account.models import CommentNotifications, OrderNotification
from rest_framework.views import APIView
from django.http import JsonResponse
from django.db.models import Q
from ALGCommon.userAuthCommon import check_login, getUser

class CheckNotificationView(APIView):

    @check_login
    def get(self, request):
        '''
        检查是否有通知
        :param request:
        :return:
        '''
        user = getUser(request.session.get('login'))
        orders = OrderNotification.objects.filter(
            Q(relatedUser=user) & Q(isRead=False)
        )
        comments = CommentNotifications.objects.filter(
            Q(aboutUser=user) & Q(isRead=False)
        )
        if (not comments.exists()) & (not orders.exists()):
            return JsonResponse({
                'status': True,
                'mss': 'none'
            }, status=404)
        else:
            return JsonResponse({
                'status': True,
                'mss': 'yes'
            })