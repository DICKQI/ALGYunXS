from rest_framework.views import APIView
from apps.account.models import User_Info
from apps.market.models import Commodity
from ALGPackage.dictInfo import model_to_dict
from django.http import JsonResponse

class CommodityView(APIView):
    def get(self, request, cid):
        '''
        获取文章详情
        :param request:
        :param cid: 商品id
        :return:
        '''
        if request.session.get('login'):
            try:
                commodity = Commodity.objects.get(id=cid)
                user = User_Info.objects.get(username__exact=request.session.get('login'))
                if commodity.seller == user:
                    editable = True
                else:
                    editable = False
                cmdResult = model_to_dict(commodity)
                return JsonResponse({
                    'result':{
                        'status':'success',
                        'editable':editable,
                        'commodity':cmdResult
                    }
                })
            except:
                return JsonResponse({'err':'找不到该内容'}, status=403)
        else:
            return JsonResponse({'err':'你还未登录'}, status=401)
