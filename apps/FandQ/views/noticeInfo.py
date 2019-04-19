from rest_framework.views import APIView
from apps.FandQ.models import Notice
from apps.account.models import User_Info
from django.http import JsonResponse
from ALGCommon.dictInfo import model_to_dict
from ALGCommon.userAuthCommon import check_login
import json


class NoticeView(APIView):
    def get(self, requests):
        '''
        获取最新的公告
        :param requests:
        :return:
        '''
        notice = Notice.objects.all()
        returnResult = model_to_dict(notice.first())
        return JsonResponse({
            'status': True,
            'notice': returnResult
        })

    @check_login
    def post(self, request):
        '''
        新增公告
        :param request:
        :return:
        '''
        params = json.loads(request.body)
        try:
            title = params.get('title')
            content = params.get('content')
        except:
            return JsonResponse({
                'status': False,
                'err': '输入错误'
            }, status=403)
        user = User_Info.objects.get(email=request.session.get("login"))
        if user.user_role != '525400':
             return JsonResponse({
                 'status': False,
                 'err': '权限限制'
             }, status=401)
        notice = Notice.objects.create(
            content=content,
            title=title,
            admin=user
        )
        return JsonResponse({
            'status': True,
            'id': notice.id
        })