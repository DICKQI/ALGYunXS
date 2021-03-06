from rest_framework.views import APIView
from apps.FandQ.models import Notice
from django.http import JsonResponse
from ALGCommon.dictInfo import model_to_dict
from ALGCommon.userAuthCommon import getUser

class NoticeControlView(APIView):
    def get(self, requests):
        '''
        获取公告列表
        :param requests:
        :return:
        '''
        if requests.session.get('login'):
            try:
                user = getUser(requests.session.get('login'))
                if user.user_role != '515400':
                    return JsonResponse({
                        'status': False,
                        'err': '你没有权限'
                    }, status=401)
                noticeList = Notice.objects.all()
                noticeListResult = [model_to_dict(notice) for notice in noticeList]
                return JsonResponse({
                    'status': True,
                    'noticeList': noticeListResult
                })
            except:
                return JsonResponse({
                    'status': False,
                    'err': '出现未知错误'
                }, status=403)
        else:
            return JsonResponse({
                'status': False,
                'err': '你还未登录'
            }, status=401)
