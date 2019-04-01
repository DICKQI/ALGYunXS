from rest_framework.views import APIView
from apps.market.models import Classification
from ALGCommon.dictInfo import model_to_dict
from ALGCommon.userCheck import check_login, authCheck, getUser
from django.http import JsonResponse
import json

class CommodityClassificationView(APIView):

    @check_login
    def post(self, requests):
        '''
        新增商品分类
        :param requests:
        :return:
        '''
        try:
            if not authCheck(['12', '515400'], requests.session.get('login')):
                return JsonResponse({
                    'status': False,
                    'err': '你没有权限'
                }, status=401)
            param = requests.body
            jsonParams = json.loads(param)
            user = getUser(requests.session.get('login'))
            if Classification.objects.filter(name__exact=jsonParams.get('name')).exists():
                return JsonResponse({
                    'status': False,
                    'err': '分类名已存在'
                }, status=401)
            classification = Classification.objects.create(
                name=jsonParams.get('name'),
                create_man=user
            )
            return JsonResponse({
                'status': True,
                'id': classification.id
            })
        except:
            return JsonResponse({
                'status': False,
                'err': '未知错误'
            }, status=403)

    @check_login
    def get(self, requests):
        '''
        获取商品分类列表
        :param requests:
        :return:
        '''
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