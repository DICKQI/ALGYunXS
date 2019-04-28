from apps.market.models import CommodityOrder, Commodity
from django.http import HttpResponse
from rest_framework.views import APIView
import datetime


class AutoOrderView(APIView):

    def get(self, request):
        '''
        超时自动确认收货
        :param request:
        :return:
        '''
        orders = CommodityOrder.objects.filter(status='已确认')
        for order in orders:
            if datetime.datetime.now() >= order.unCompleteDeadline:
                order.status = '已完成'
                order.save()
        return HttpResponse('好哦好哦')

    def delete(self, request):
        orders = CommodityOrder.objects.filter(status='未确认')
        for order in orders:
            if datetime.datetime.now() >= order.unConfirmDeadline:
                order.status = '已取消'
                order.save()
                order.commodity.status = 's'
                order.commodity.save()
        return HttpResponse('嘿嘿嘿')
