from rest_framework.views import APIView
from django.http import JsonResponse

class LogoutViews(APIView):
    def get(self, request):
        '''登出账户'''
        if request.session.get('login'):
            request.session['login'] = None
            return JsonResponse({'result':{
                'status':'success'
            }})
        else:
            return JsonResponse({'err':'你还未登录呢'})