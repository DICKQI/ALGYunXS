from rest_framework.views import APIView
from apps.account.models import User_Info
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse


class RegisterView(APIView):
    def post(self, request):
        '''注册账户'''
        params = request.POST
        try:
            User_Info.objects.get(username__exact=params['username'])
            return JsonResponse({
                'status':False,
                'err':'用户名已存在'
            }, status=401)
        except:
            try:
                hash_password = make_password(params.get('password'))
                newUser = User_Info.objects.create(
                    username=params.get('username'),
                    password=hash_password,
                    email=params.get('email'),
                    nickname=params.get('nickname'),
                    phone_number=params.get('phone_number'),
                )

                return JsonResponse({
                    'status':True,
                    'id':newUser.id,
                    'username':newUser.username,
                    'nickname':newUser.nickname,
                })
            except:
                return JsonResponse({
                    'status':False,
                    'err': '出现了预期之外的错误'
                }, status=403)