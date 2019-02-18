from rest_framework.views import APIView
from apps.account.models import User_Info, EmailVerifyRecord
from django.http import JsonResponse


class ActiveView(APIView):
    def get(self, request, a_code):
        '''
        认证账户
        :param request:
        :param a_code:
        :return:
        '''
        if request.session.get('login') != None:
            try:
                record = EmailVerifyRecord.objects.get(code__exact=a_code)
                if record.code_status == 'used' or record.send_type == 'forget':
                    return JsonResponse({
                        'status': False,
                        'err': '激活失败'
                    })
                user = User_Info.objects.get(email=request.session.get('login'))
                if record.email == user.email:
                    user.user_role = '4'
                    user.save()
                    record.code_status = 'used'
                    record.save()
                    return JsonResponse({'result': {
                        'status': True,
                        'id': user.id
                    }})
                else:
                    return JsonResponse({
                        'status': False,
                        'err': '激活失败'
                    })
            except:
                return JsonResponse({
                    'status': False,
                    'err': '激活失败'
                })
        else:
            return JsonResponse({
                'status': False,
                'err': '您还未登录呢'
            })
