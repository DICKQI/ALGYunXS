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
        if requests.session.get('login') != None:
            ptjAll = PTJInfo.objects.all()
            page = requests.GET.get('page')
            ptjPage = Paginator(ptjAll, 5)
            try:
                ptjList = ptjPage.page(page)
            except PageNotAnInteger:
                ptjList = ptjPage.page(1)
            except EmptyPage:
                ptjList = ptjPage.page(1)

            ptj = [model_to_dict(ptjs, exclude='create_time') for ptjs in ptjList if ptjs.status == 'p']

            return JsonResponse({
                'status': True,
                'ptjList': ptj
            })
        else:
            return JsonResponse({
                'status': False,
                'err': '你还未登录'
            }, status=401)
