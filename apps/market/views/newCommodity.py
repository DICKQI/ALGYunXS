from rest_framework.views import APIView
from apps.account.models import User_Info
from apps.market.models import Commodity, Classification
from django.http import JsonResponse
class NewCommodityView(APIView):
    def post(self, request):
        '''
        新增文章
        :param request:
        :param cid:
        :return:
        '''
        if request.session.get('login'):
            params = request.POST
            if params.get('name') == None or params.get('c_detail') == None or params.get('classification') == None:
                return JsonResponse({
                    'status':False,
                    'err': '输入错误'
                }, status=403)
            try:
                seller = User_Info.objects.get(username__exact=request.session.get('login'))
                try:
                    classification = Classification.objects.get(name__exact=params.get('classification'))
                except:
                    return JsonResponse({
                        'status':False,
                        'err': '找不到该分类'
                    })
                if params.get('status') != None:
                    status = params.get('status')
                else:
                    status = 's'
                newCommodity = Commodity.objects.create(
                    seller=seller,
                    name=params.get('name'),
                    c_detail=params.get('c_detail'),
                    classification=classification,
                    status=status
                )
                return JsonResponse({
                    'status': True,
                    'commodity': newCommodity.id
                })
            except:
                return JsonResponse({
                    'status':False,
                    'err': '未知错误'
                }, status=403)
        else:
            return JsonResponse({
                'status':False,
                'err': '你还未登录'
            }, status=401)