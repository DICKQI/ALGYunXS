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
        orders = CommodityOrder.objects.filter(status='已下单')
        for order in orders:
            if datetime.datetime.now() >= order.unConfirmDeadline:
                order.status = '已完成'
                order.save()
        return HttpResponse('好哦好哦')
