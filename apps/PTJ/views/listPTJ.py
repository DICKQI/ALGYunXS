from rest_framework.views import APIView
from django.http import JsonResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from ALGPackage.dictInfo import model_to_dict
from apps.PTJ.models import PTJInfo

class ListPTJ(APIView):

    def get(self, requests):
        '''
        获取兼职消息列表
        :param requests:
        :return:
        '''

