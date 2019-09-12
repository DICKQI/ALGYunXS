from rest_framework.views import APIView
from django.http import JsonResponse
from ALGCommon.paginator import paginator
from ALGCommon.dictInfo import model_to_dict
from apps.PTJ.models import PTJInfo


class ListPTJ(APIView):

    def get(self, requests):
        '''
        获取兼职消息列表
        :param requests:
        :return:
        '''
        ptjAll = PTJInfo.objects.all()
        page = requests.GET.get('page')
        ptjList = paginator(ptjAll, page)

        ptj = [model_to_dict(ptjs, exclude='create_time') for ptjs in ptjList if ptjs.status == 'p']

        return JsonResponse({
            'status': True,
            'ptjList': ptj
        })
