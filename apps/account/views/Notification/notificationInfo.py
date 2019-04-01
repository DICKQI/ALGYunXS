from apps.account.models import CommentNotifications, OrderNotification, User_Info
from apps.market.models import CommodityOrder, Commodity
from apps.helps.models import Article, AComment
from apps.PTJ.models import PTJInfo
from rest_framework.views import APIView
from django.http import JsonResponse
from django.db.models import Q
from ALGCommon.userCheck import check_login, getUser
from ALGCommon.dictInfo import model_to_dict


class NotificationView(APIView):
    orderNotificationFields = [
        'relatedCommodityID', 'relatedOrderID', 'noticeTime', 'id'
    ]

    commentNotificationFields = [
        'relatedID', 'type', 'id'
    ]

    @check_login
    def get(self, request):
        '''
        获取通知
        :param request:
        :return:
        '''
        '''获取订单通知'''
        user = getUser(request.session.get('login'))
        orders = OrderNotification.objects.filter(
            Q(relatedUser=user) & Q(isRead=False)
        )
        order_notification = [model_to_dict(order, fields=self.orderNotificationFields) for order in orders]
        '''获取评论通知'''
        comments = CommentNotifications.objects.filter(
            Q(aboutUser=user) & Q(isRead=False)
        )
        comment_notification = [model_to_dict(comment, fields=self.commentNotificationFields) for comment in comments]

        return JsonResponse({
            'status': True,
            'orderNotification': order_notification,
            'commentNotification': comment_notification
        })

    @check_login
    def put(self, nid, type):
        '''
        通知已读
        :param nid:
        :param type:
        :return:
        '''
        if isinstance(type, str):
            if type == 'comment':
                pass
            elif type == 'order':
                pass
        else:
            return JsonResponse({
                'status': False,
                'err': '参数错误'
            }, status=403)

