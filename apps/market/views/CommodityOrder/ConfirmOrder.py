from apps.market.models import Commodity, CommodityOrder
from django.http import JsonResponse
from rest_framework.views import APIView
from ALGCommon.userAuthCommon import check_login, getUser
from .OrderInfo import OrderView
from datetime import datetime as da
from datetime import timedelta
import json

class ConfirmOrderView(APIView):

    @check_login
    def get(self, request, cid, ocid, type):
        '''
        卖家确认/发货订单
        :param request:
        :param cid:
        :param ocid:
        :return:
        '''
        classOrder = OrderView()
        order = classOrder.getOrder(cid, ocid)
        if not order:
            return JsonResponse({
                'status': False,
                'err': '订单未找到'
            }, status=404)
        user = getUser(request.session.get('login'))
        if user != order.commodity.seller:
            return JsonResponse({
                'status': False,
                'err': '你没有权限操作'
            }, status=401)
        if type == 'c':
            order.status = '已确认'
        elif type == 'd':
            order.status = '已发货'
        else:
            return JsonResponse({
                'status': False,
                'err': '参数错误'
            })
        '''设置自动确认收货截止时间'''
        order.unCompleteDeadline = da.now() + timedelta(days=15)
        order.save()
        return JsonResponse({
            'status': True,
            'id': order.id
        })

