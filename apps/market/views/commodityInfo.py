from rest_framework.views import APIView
from apps.account.models import User_Info
from apps.market.models import Commodity, Classification
from ALGPackage.dictInfo import model_to_dict
import datetime
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
                commodity.views += 1
                commodity.save()
                cmdResult = model_to_dict(commodity)
                return JsonResponse({
                    'status':'success',
                    'editable':editable,
                    'commodity':cmdResult
                })
            except:
                return JsonResponse({'err':'找不到该内容'}, status=403)
        else:
            return JsonResponse({'err':'你还未登录'}, status=401)
    def put(self, request, cid):
        '''
        修改文章内容
        :param request:
        :param cid:
        :return:
        '''
        if request.session.get('login'):
            params = request.POST
            if params.get('c_detail') == None:
                return JsonResponse({'err':'input error'}, status=403)
            try:
                commodity = Commodity.objects.get(id=cid)
                commodity.c_detail = params.get('c_detail')
                if params.get('classification') != None:
                    try:
                        commodity.classification = Classification.objects.get(name__exact=params.get('classification'))
                    except:
                        return JsonResponse({'err':'不存在此分类名'}, status=403)
                if params.get('status') != None:
                    commodity.status = params.get('status')
                commodity.last_mod_time = datetime.datetime.now()
                commodity.save()
                return JsonResponse({
                    'id':commodity.id,
                    'after detail':commodity.c_detail,
                    'status':commodity.status,
                    'classification':commodity.classification.name
                })
            except:
                return JsonResponse({'err': '找不到该内容'}, status=403)
        else:
            return JsonResponse({'err':'你还未登录'}, status=401)
    def delete(self, request, cid):
        '''
        删除商品
        :param request:
        :param cid:
        :return:
        '''
        if request.session.get('login'):
            try:
                commodity = Commodity.objects.get(id=cid)
                user = User_Info.objects.get(username__exact=request.session.get('login'))
                if commodity.seller != user:
                    return JsonResponse({'err':'你没有权限'})
                commodity.delete()
                return JsonResponse({
                    'status':'success',
                    'id':cid
                })
            except:
                return JsonResponse({'err':'未知错误'})
        else:
            return JsonResponse('你还未登录呢')