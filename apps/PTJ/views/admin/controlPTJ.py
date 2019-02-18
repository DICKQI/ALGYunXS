from apps.account.models import User_Info
from apps.PTJ.models import PTJInfo
from rest_framework.views import APIView
from django.http import JsonResponse
import json

class ControlPTJView(APIView):

    def put(self, requests, cid):
        '''
        管理员更改兼职信息状态
        :param requests:
        :param cid:
        :return:
        '''
        if requests.session.get('login'):
            try:
                user = User_Info.objects.get(email=requests.session.get('login'))
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
        else:
            return JsonResponse({
                'status': False,
                'err': '你没有权限'
            }, status=401)