from rest_framework.views import APIView
from apps.account.models import User_Info, EmailVerifyRecord
from .send_email import SendView
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password
import json

class ResetView(APIView):
    def post(self, request, r_code):
        '''
        重置密码
        :param request:
        :return:
        '''
        if request.session.get('login') != None:
            user = User_Info.objects.get(username__exact=request.session.get('login'))
            try:
                record = EmailVerifyRecord.objects.get(code__exact=r_code)
                if record.code_status == 'used' or record.send_type == 'active':
                    return JsonResponse({
                        'status':False,
                        'err': '重置失败'
                    }, status=404)
                if record.email == user.email:
                    params = request.body
                    jsonParams = json.loads(params)
                    if params.get('password') != None:
                        key = make_password(jsonParams.get('password'))
                        user.password = key
                        user.save()
                        record.code_status = 'used'
                        record.save()
                        return JsonResponse({'result':{
                            'status':True,
                            'id':user.id
                        }})
                    else:
                        return JsonResponse({
                            'status':False,
                            'err': 'input error'
                        }, status=404)
                else:
                    return JsonResponse({
                        'status':False,
                        'err': '重置失败'
                    }, status=404)
            except:
                return JsonResponse({
                    'status':False,
                    'err': '重置失败'
                }, status=404)
        else:
            return JsonResponse({
                'status':False,
                'err': '你还未登录'
            }, status=401)