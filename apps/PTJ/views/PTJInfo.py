from rest_framework.views import APIView
from apps.PTJ.models import *
from ALGCommon.dictInfo import model_to_dict
from django.http import JsonResponse


class PTJInfoView(APIView):

    def get(self, requests, pid):
        '''
        获得兼职消息详情
        :param requests:
        :param pid: ptj id
        :return:
        '''
        if requests.session.get('login') != None:
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
        else:
            return JsonResponse({
                'status': False,
                'err': '你还未登录'
            }, status=401)
    def delete(self, requests, pid):
        '''
        删除兼职消息
        :param requests:
        :param pid:
        :return:
        '''
        if requests.session.get('login') != None:
            try:
                user = User_Info.objects.get(email=requests.session.get('login'))
                try:
                    ptj = PTJInfo.objects.get(id=pid)
                except:
                    return JsonResponse({
                        'status': False,
                        'err': '内容不存在'
                    }, status=404)
                if ptj.publisher != user:
                    if user.user_role != '525400' or user.user_role != '1234':
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
        else:
            return JsonResponse({
                'status': False,
                'err': '你还未登录'
            }, status=401)