from rest_framework.views import APIView
from apps.account.models import User_Info
from apps.market.models import Commodity, Classification
from ALGPackage.dictInfo import model_to_dict
from django.utils.timezone import now
from django.http import JsonResponse
import json


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
                return JsonResponse({
                    'status': False,
                    'err': '找不到该内容'
                }, status=404)
            user = User_Info.objects.get(phone_number__exact=request.session.get('login'))
            if user != commodity.seller:
                if commodity.status == 's':
                    # 未发布的商品无法直接查看
                    return JsonResponse({
                        'status': False,
                        'err': '找不到该内容'
                    }, status=404)
            if commodity.seller == user:
                editable = True
            else:
                editable = False
            commodity.views += 1
            commodity.save()
            cmdResult = model_to_dict(commodity,exclude='status')
            return JsonResponse({
                'status': True,
                'editable': editable,
                'commodity': cmdResult
            })
        else:
            return JsonResponse({
                'status': False,
                'err': '你还未登录'
            }, status=401)

    def put(self, request, cid):
        '''
        修改文章内容
        :param request:
        :param cid:
        :return:
        '''
        if request.session.get('login'):
            params = request.body
            jsonParams = json.loads(params)
            try:
                commodity = Commodity.objects.get(id=cid)
                user = User_Info.objects.get(phone_number__exact=request.session.get('login'))
                if commodity.seller != user:
                    if user.user_role != '12' or user.user_role != '525400':
                        return JsonResponse({
                            'status': False,
                            'err': '你没有权限'
                        })
                    else:
                        pass
                if jsonParams.get('c_detail'):
                    commodity.c_detail = jsonParams.get('c_detail')
                if jsonParams.get('classification'):
                    try:
                        commodity.classification = Classification.objects.get(name__exact=jsonParams.get('classification'))
                    except:
                        return JsonResponse({
                            'status': False,
                            'err': '不存在此分类名'
                        }, status=404)
                if jsonParams.get('status'):
                    commodity.status = jsonParams.get('status')
                if jsonParams.get('name'):
                    commodity.name = jsonParams.get('name')
                commodity.last_mod_time = now()
                commodity.save()
                return JsonResponse({
                    'status': True,
                    'id': commodity.id,
                    'name': commodity.name,
                    'after detail': commodity.c_detail,
                    'commodity_status': commodity.status,
                    'classification': commodity.classification.name
                })
            except:
                return JsonResponse({
                    'status': False,
                    'err': '意料之外的错误'
                }, status=403)
        else:
            return JsonResponse({
                'status': False,
                'err': '你还未登录'
            }, status=401)

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
                user = User_Info.objects.get(phone_number__exact=request.session.get('login'))
                if commodity.seller != user:
                    if user.user_role != '12' or user.user_role != '525400':
                        return JsonResponse({
                            'status': False,
                            'err': '你没有权限'
                        }, status=401)
                commodity.delete()
                return JsonResponse({
                    'status': True,
                    'result': '已删除' + cid + '号文章'
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