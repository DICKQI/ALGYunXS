from apps.tailwind.models import *
from django.http import JsonResponse
from rest_framework.views import APIView
from ALGCommon.userAuthCommon import *
from ALGCommon.dictInfo import model_to_dict
from ALGCommon.paginator import paginator


class TailwindInfoView(APIView):

    def get(self, request):
        '''
        获取有闲订单列表
        :param request:
        :param tid:
        :return:
        '''
