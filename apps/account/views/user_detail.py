from apps.account.models import User_Info
from django.http import JsonResponse
from rest_framework.views import APIView
from ALGPackage.dictInfo import model_to_dict
class MeView(APIView):
    USER_INCLUDE_FIELDS = [
        'nickname', 'phone_number', 'student_id', 'age',
        'credit_score', 'last_login_time'
    ]
    def get(self, request):
        '''
        获取当前登录用户信息
        :param request:
        :return:
        '''
        if request.session.get('login') != None:
            try:
                user = User_Info.objects.get(username__exact=request.session.get('login'))
                userResult = model_to_dict(user, fields=self.USER_INCLUDE_FIELDS)
                if user.head_portrait:
                    userResult['head'] = 'https://algyunxs.oss-cn-shenzhen.aliyuncs.com/media/' + str(
                        user.head_portrait) + '?x-oss-process=style/head_portrait'
                else:
                    userResult['head'] = None
                return JsonResponse({'myself':userResult})
            except:
                return JsonResponse({'err':'意料之外的错误'}, status=403)
        else:
            return JsonResponse({'err':'还没登录'}, status=401)
