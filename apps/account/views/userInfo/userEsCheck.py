from apps.account.models import User_Info
from rest_framework.views import APIView
from django.http import JsonResponse
from ..esCheck import es_test
from ALGCommon.userCheck import check_login
import json


class ESCheckView(APIView):
    @check_login
    def post(self, requests):
        '''
        验证教务账号
        :param requests:
        :return:
        '''
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
