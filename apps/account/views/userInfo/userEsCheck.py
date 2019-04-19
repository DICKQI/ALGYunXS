from rest_framework.views import APIView
from django.http import JsonResponse
from ..esCheck import es_test
from ALGCommon.userAuthCommon import check_login, getUser
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
        esResult = es_test(params.get('school'), params.get('username'), params.get('password')).result()
        if esResult:
            user = getUser(requests.session.get('login'))
            user.student_id = params.get('username')
            user.RealName = esResult.get('name')
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
