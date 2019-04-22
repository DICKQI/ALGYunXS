from rest_framework.views import APIView
from apps.PTJ.models import *
from ALGCommon.dictInfo import model_to_dict
from ALGCommon.userAuthCommon import check_login, getUser
from django.http import JsonResponse
import json

class PTJInfoView(APIView):

    @check_login
    def get(self, requests, pid):
        '''
        获得兼职消息详情
        :param requests:
        :param pid: ptj id
        :return:
        '''
        try:
            try:
                pObject = PTJInfo.objects.get(id=pid)
            except:
                return JsonResponse({
                    'status': False,
                    'err': '内容不存在'
                }, status=404)

            ptjResult = model_to_dict(pObject)

            return JsonResponse({
                'status': True,
                'ptj': ptjResult
            })

        except:
            return JsonResponse({
                'status': False,
                'err': '出现未知的错误'
            }, status=403)

    @check_login
    def delete(self, requests, pid):
        '''
        删除兼职消息
        :param requests:
        :param pid:
        :return:
        '''
        try:
            user = getUser(requests.session.get('login'))
            try:
                ptj = PTJInfo.objects.get(id=pid)
            except:
                return JsonResponse({
                    'status': False,
                    'err': '内容不存在'
                }, status=404)
            if ptj.publisher != user:
                if user.user_role != '525400':
                    return JsonResponse({
                        'status': False,
                        'err': '你没有权限'
                    }, status=401)
            ptj.delete()
            return JsonResponse({
                'status': True,
                'id': pid
            })
        except:
            return JsonResponse({
                'status': False,
                'err': '出现未知的错误'
            }, status=403)

    @check_login
    def post(self, requests):
        '''
        新增兼职信息
        :param requests:
        :return:
        '''
        try:
            param = requests.body
            jsonParam = json.loads(param)

            user = getUser(requests.session.get('login'))

            if user.user_role != '515400' or user.user_role != '1234':
                return JsonResponse({
                    'status': False,
                    'err': '你没有权限'
                }, status=401)

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