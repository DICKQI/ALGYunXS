from rest_framework.views import APIView
from apps.FandQ.models import Notice
from django.http import JsonResponse
from ALGCommon.dictInfo import model_to_dict

class NoticeView(APIView):
    def get(self, requests):
        '''
        获取最新的公告
        :param requests:
        :return:
        '''
        notice = Notice.objects.all()
        returnResult = model_to_dict(notice.first())
        return JsonResponse({
            'status':True,
            'notice':returnResult
        })
