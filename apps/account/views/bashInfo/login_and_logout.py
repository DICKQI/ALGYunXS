from rest_framework.views import APIView
from apps.account.models import User_Info
from apps.log.models import LoginLog
from ALGCommon.userCheck import check_login
from django.http import JsonResponse
from django.contrib.auth.hashers import check_password
from django.utils.timezone import now
from django.db.models import Q
import json


class BaseViews(APIView):
    def post(self, request):
        '''
        登录账户
        :param request:
        :return:
        '''

        try:
            jsonParams = json.loads(request.body)
            # 可以使用id或者邮箱登录
            user = User_Info.objects.filter(
                Q(email__exact=jsonParams.get('email')) |
                Q(id=jsonParams.get('id'))
            )
            if user.exists():
                user = user[0]
            else:
                return JsonResponse({
                    'status': False,
                    'err': '无此用户'
                }, status=403)
            if user.user_role == '6':
                return JsonResponse({
                    'status': False,
                    'err': '此账号已被封禁，请联系管理员'
                }, status=403)
            if check_password(jsonParams.get('password'), user.password):
                request.session['login'] = user.email
                user.last_login_time = now()
                user.save()
                '''记录登录信息'''
                ip = request.META['REMOTE_ADDR']
                device = jsonParams.get('device')
                LoginLog.objects.create(
                    ip=ip,
                    user=user,
                    login_device=device
                )
                return JsonResponse({
                    'status': True,
                    'id': user.id,
                    'email':user.email
                })
            else:
                return JsonResponse({
                    'status': False,
                    'err': '密码错误'
                }, status=401)
        except:
            return JsonResponse({
                'status': False,
                'err': '出现了预期以外的错误'
            }, status=403)

    @check_login
    def delete(self, request):
        '''
        登出账户
        :param request:
        :return:
        '''
        user = User_Info.objects.get(email=request.session.get('login'))
        request.session['login'] = None
        return JsonResponse({
            'status': True,
            'id': user.id
        })
