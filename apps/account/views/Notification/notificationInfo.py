from apps.account.models import CommentNotifications, OrderNotification
from rest_framework.views import APIView
from django.http import JsonResponse
from django.db.models import Q
from ALGCommon.userAuthCommon import check_login, getUser
from ALGCommon.dictInfo import model_to_dict


class NotificationView(APIView):
    orderNotificationFields = [
        'relatedCommodityID', 'relatedOrderID', 'noticeTime', 'id'
    ]

    commentNotificationFields = [
        'relatedID', 'type', 'id', 'noticeTime'
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
        comments = CommentNotifications.objects.filter(
            Q(aboutUser=user) & Q(isRead=False)
        )

        order_notification = [model_to_dict(order, fields=self.orderNotificationFields) for order in orders]
        '''获取评论通知'''
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
        if type == 'comment':
           comment_notification = CommentNotifications.objects.filter(id=nid)
           if not comment_notification.exists():
               return JsonResponse({
                   'status': False,
                   'err': '通知不存在'
               })
           comment_notification = comment_notification[0]
           comment_notification.isRead = True
           comment_notification.save()
           return JsonResponse({
               'status': True,
               'id': comment_notification.id
           })
        elif type == 'order':
            order_notification = OrderNotification.objects.filter(id=nid)
            if not order_notification.exists():
                return JsonResponse({
                    'status': False,
                    'err': '通知不存在'
                })
            order_notification = order_notification[0]
            order_notification.isRead = True
            order_notification.save()
            return JsonResponse({
                'status': True,
                'id': order_notification.id
            })