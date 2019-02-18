from apps.account.models import User_Info
from rest_framework.views import APIView
from django.http import JsonResponse
from ..esCheck import es_test
import json


class ESCheckView(APIView):
    def post(self, requests):
        '''
        验证教务账号
        :param requests:
        :return:
        '''
        if requests.session.get('login'):
            params = json.loads(requests.body)

            if es_test(params.get('school'), params.get('username'), params.get('password')).result():
                user = User_Info.objects.get(email=requests.session.get('login'))
                user.student_id = params.get('username')
                user.save()
                return JsonResponse({
                    'status': True,
                    'id': user.id
                })
            else:
                return JsonResponse({
                    'status': False,
                    'err': '验证失败，请重试'
                }, status=403)
        else:
            return JsonResponse({
                'status': False,
                'err': '你还未登录呢'
            }, status=401)
