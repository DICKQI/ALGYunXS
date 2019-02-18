from rest_framework.views import APIView
from apps.account.models import User_Info
from apps.PTJ.models import *
from ALGCommon.dictInfo import model_to_dict
from django.http import JsonResponse
import json

class NewPTJView(APIView):
    def post(self, requests):
        '''
        新增兼职信息
        :param requests:
        :return:
        '''
        if requests.session.get('login') != None:
            try:
                param = requests.body
                jsonParam = json.loads(param)

                user = User_Info.objects.get(email=requests.session.get('login'))

                ptj = PTJInfo.objects.create(
                    publisher=user,
                    title=jsonParam.get('title'),
                    content=jsonParam.get('content')
                )
                return JsonResponse({
                    'status': True,
                    'id': ptj.id
                })

            except:
                return JsonResponse({
                    'status': False,
                    'err': '出现未知的错误'
                }, status=403)
        else:
            return JsonResponse({
                'status': False,
                'err': '你还未登录'
            }, status=401)