from rest_framework.views import APIView
from apps.account.models import User_Info
from apps.market.models import Classification
from ALGCommon.dictInfo import model_to_dict
from django.http import JsonResponse
import json

class CommodityClassificationView(APIView):

    def post(self, requests):
        '''
        新增商品分类
        :param requests:
        :return:
        '''
        if requests.session.get('login') != None:
            try:
                user = User_Info.objects.get(email=requests.session.get('login'))
                if user.user_role == '12' or user.user_role == '515400':
                    param = requests.body
                    jsonParams = json.loads(param)
                    if Classification.objects.filter(name__exact=jsonParams.get('name')).exists():
                        return JsonResponse({
                            'status': False,
                            'err': '分类名已存在'
                        })
                    classification = Classification.objects.create(name=jsonParams.get('name'))
                    return JsonResponse({
                        'status': True,
                        'id': classification.id
                    })
                else:
                    return JsonResponse({
                        'status': False,
                        'err': '你没有权限'
                    }, status=401)
            except:
                return JsonResponse({
                    'status': False,
                    'err': '未知错误'
                }, status=403)
        else:
            return JsonResponse({
                'status': False,
                'err': '你还未登录呢'
            }, status=401)

    def get(self, requests):
        '''
        获取商品分类列表
        :param requests:
        :return:
        '''
        if requests.session.get('login') != None:
            try:
                classificationAll = Classification.objects.all()
                result = [model_to_dict(classification) for classification in classificationAll]
                return JsonResponse({
                    'status':True,
                    'classificationList':result
                })
            except:
                return JsonResponse({
                    'status': False,
                    'err': '未知错误'
                }, status=403)
        else:
            return JsonResponse({
                'status': False,
                'err': '你还未登录呢'
            }, status=401)