from apps.account.models import User_Info
from apps.PTJ.models import PTJInfo
from rest_framework.views import APIView
from django.http import JsonResponse
from ALGCommon.userCheck import check_login, getUser
import json

class ControlPTJView(APIView):

    @check_login
    def put(self, requests, cid):
        '''
        管理员更改兼职信息状态
        :param requests:
        :param cid:
        :return:
        '''
        try:
            user = getUser(requests.session.get('login'))
            if user.user_role != '515400' or user.user_role != '1234':
                return JsonResponse({
                    'status': False,
                    'err': '你没有权限'
                }, status=401)
            try:
                ptj = PTJInfo.objects.get(id=cid)
            except:
                return JsonResponse({
                    'status': False,
                    'err': '内容不存在'
                }, status=404)

            param = requests.body
            jsonParam = json.loads(param)

            ptj.status = jsonParam.get('status')

            ptj.save()

            return JsonResponse({
                'status': True,
                'result': '修改成功'
            })

        except:
            return JsonResponse({
                'status': False,
                'err': '意料之外的错误'
            })