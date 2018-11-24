from rest_framework.views import APIView
from apps.account.models import User_Info
from django.http import JsonResponse
from django.contrib.auth.hashers import check_password

class LoginViews(APIView):
    def post(self, request):
        '''
        登录账户
        :param request:
        :return:
        '''
        params = request.POST
        try:
            try:
                User_Info.objects.get(username__exact=params.get('username'))
            except:
                return JsonResponse({'err':'无此用户'}, status=403)
            user = User_Info.objects.get(username__exact=params.get('username'))
            if user.user_role == 6:
                return JsonResponse({'err':'此账号已被封禁，请联系管理员'}, status=403)
            if check_password(params.get('password'), user.password):
                request.session['login'] = user.username
                return JsonResponse({'result':{
                    'status':'success',
                    'id':user.id,
                }})
            else:
                return JsonResponse({'err':'密码错误'}, status=401)
        except:
            return JsonResponse({'err':'出现了预期以外的错误'}, status=403)
    def delete(self, request):
        '''
        登出账户
        :param request:
        :return:
        '''
        if request.session.get('login'):
            user = User_Info.objects.get(username__exact=request.session.get('login'))
            request.session['login'] = None
            return JsonResponse({
                'status':'success',
                'id':user.id
            })
        else:
            return JsonResponse({'err':'你还未登录呢'}, status=401)