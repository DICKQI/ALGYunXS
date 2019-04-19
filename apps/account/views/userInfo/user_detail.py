from apps.account.models import User_Info
from django.http import JsonResponse
from rest_framework.views import APIView
from ALGCommon.dictInfo import model_to_dict
from ALGCommon.userAuthCommon import check_login
import time


class MeView(APIView):

    USER_INCLUDE_FIELDS = [
        'nickname', 'email', 'student_id', 'age',
        'credit_score', 'last_login_time', 'from_school'
    ]
    @check_login
    def get(self, request):
        '''
        获取当前登录用户信息
        :param request:
        :return:
        '''
        user = User_Info.objects.get(email=request.session.get('login'))
        userResult = model_to_dict(user, fields=self.USER_INCLUDE_FIELDS)
        if user.head_portrait:
            userResult['head'] = 'https://algyunxs.oss-cn-shenzhen.aliyuncs.com/media/' + str(
                user.head_portrait) + '?x-oss-process=style/head_portrait'

        '''检查是否有未读通知'''
        return JsonResponse({
            'status': True,
            'myself': userResult,
        })
