from apps.tailwind.models import TailwindUserConfig
from django.http import JsonResponse
from rest_framework.views import APIView
from ALGCommon.userAuthCommon import getUser, check_login, authCheck, studentCheck
from ALGCommon.dictInfo import model_to_dict
from ALGCommon.paginator import paginator

class TailwindUserView(APIView):

    @check_login
    def post(self, request):
        '''
        为初次进入有闲的用户创建有闲账户
        :param request:
        :return:
        '''
        user = getUser(request.session.get('login'))
        if not studentCheck(user):
            return JsonResponse({
                'status': False,
                'err': '请完成学生认证'
            }, status=403)
        