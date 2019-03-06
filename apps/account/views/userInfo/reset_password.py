from rest_framework.views import APIView
from apps.account.models import User_Info, EmailVerifyRecord
from ALGCommon.check_login import check_login
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password
import json


class ResetView(APIView):
    def post(self, request):
        '''
        忘记密码后重置密码
        :param request:
        :return:
        '''
        params = request.body
        jsonParams = json.loads(params)
        # if request.session.get('login'):
        #     user = User_Info.objects.get(email=request.session.get('login'))
        # else:
        user = User_Info.objects.get(email__exact=jsonParams.get('email'))
        record = EmailVerifyRecord.objects.filter(code__exact=jsonParams.get('r_code'))
        if not record.exists():
            return JsonResponse({
                'status': False,
                'err': '重置失败'
            }, status=404)
        record.code_status = 'used'
        record.save()

        key = make_password(jsonParams.get('password'))
        user.password = key
        user.save()
        return JsonResponse({'result': {
            'status': True,
            'id': user.id
        }})

    @check_login
    def get(self, request, r_code):
        '''
        检查重置密码验证码正确性
        :param request:
        :param r_code:
        :return:
        '''
        user = User_Info.objects.get(email=request.session.get('login'))
        record = EmailVerifyRecord.objects.filter(code__exact=r_code)
        if not record.exists():
            return JsonResponse({
                'status': False,
                'err': '重置失败'
            }, status=404)
        if record.code_status == 'used' or record.send_type == 'active':
            return JsonResponse({
                'status': False,
                'err': '重置失败'
            }, status=404)
        if record.email == user.email:
            return JsonResponse({
                'status': True,
                'email': user.email
            })
        else:
            return JsonResponse({
                'status': False,
                'err': '重置失败'
            }, status=404)
