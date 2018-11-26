from rest_framework.views import APIView
from apps.account.models import User_Info
from apps.market.models import Commodity, Classification
from ALGPackage.dictInfo import model_to_dict
from django.utils.timezone import now
from django.http import JsonResponse
from django.db.models import F

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
            except:
                return JsonResponse({'err': '找不到该内容'}, status=403)
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
                return JsonResponse({'err':'商品详情不能为空'}, status=403)
            try:
                commodity = Commodity.objects.get(id=cid)
                user = User_Info.objects.get(username__exact=request.session.get('login'))
                if commodity.seller != user:
                    if user.user_role != '12' or user.user_role != '525400':
                        return JsonResponse({'err':'你没有权限'})
                    else:
                        pass
                commodity.c_detail = params.get('c_detail')
                if params.get('classification') != None:
                    try:
                        commodity.classification = Classification.objects.get(name__exact=params.get('classification'))
                    except:
                        return JsonResponse({'err':'不存在此分类名'}, status=403)
                if params.get('status') != None:
                    commodity.status = params.get('status')
                if params.get('name') != None:
                    commodity.name = params.get('name')
                commodity.last_mod_time = now()
                commodity.save()
                return JsonResponse({
                    'id':commodity.id,
                    'name':commodity.name,
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
                    if user.user_role != '12' or user.user_role != '525400':
                        return JsonResponse({'err':'你没有权限'})
                    else:
                        pass
                commodity.delete()
                return JsonResponse({
                    'status':'success',
                    'id':cid
                })
            except:
                return JsonResponse({'err':'未知错误'})
        else:
            return JsonResponse('你还未登录呢')