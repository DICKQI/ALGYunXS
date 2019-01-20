from rest_framework.views import APIView
from apps.account.models import User_Info
from apps.market.models import Commodity, Classification
from django.http import JsonResponse
import json


class NewCommodityView(APIView):
    def post(self, request):
        '''
        新增文章
        :param request:
        :param cid:
        :return:
        '''
        if request.session.get('login'):
            param = request.body
            jsonParams = json.loads(param)
            if jsonParams.get('name') == None or jsonParams.get('c_detail') == None or jsonParams.get('classification') == None:
                return JsonResponse({
                    'status': False,
                    'err': '输入错误'
                }, status=403)
            try:
                seller = User_Info.objects.get(phone_number__exact=request.session.get('login'))
                try:
                    classification = Classification.objects.get(name__exact=jsonParams.get('classification'))
                except:
                    return JsonResponse({
                        'status': False,
                        'err': '找不到该分类'
                    })
                if jsonParams.get('status') != None:
                    status = jsonParams.get('status')
                else:
                    status = 's'
                newCommodity = Commodity.objects.create(
                    seller=seller,
                    name=jsonParams.get('name'),
                    c_detail=jsonParams.get('c_detail'),
                    classification=classification,
                    status=status
                )
                return JsonResponse({
                    'status': True,
                    'commodity': newCommodity.id
                })
            except:
                return JsonResponse({
                    'status': False,
                    'err': '未知错误'
                }, status=403)
        else:
            return JsonResponse({
                'status': False,
                'err': '你还未登录'
            }, status=401)
