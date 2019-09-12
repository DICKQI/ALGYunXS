from apps.account.models import User_Info
from rest_framework.views import APIView
from django.http import JsonResponse
from ALGCommon.userAuthCommon import check_login, authCheck
from ALGCommon.dictInfo import model_to_dict


class UserStatisticsView(APIView):

    INCLUDE_FIELDS = [
        'id', 'email', 'nickname', 'joined_date', 'student_id', 'RealName', 'credit_score'
    ]

    @check_login
    def get(self, request):
        '''
        获取用户列表
        :param request:
        :return:
        '''
        if authCheck(role='515400', email=request.session.get('login')):
            userList = User_Info.objects.all()
            return JsonResponse({
                'status': True,
                'users': [model_to_dict(user, fields=self.INCLUDE_FIELDS) for user in userList]
            })
        else:
            return JsonResponse({
                'status': False,
                'err': '你没有权限'
            }, status=401)
