from rest_framework.views import APIView
from apps.account.models import User_Info
from apps.market.models import Commodity, Classification
from apps.log.models import CommodityViewLog
from ALGCommon.dictInfo import model_to_dict
from django.utils.timezone import now
from django.http import JsonResponse
import json


class CommodityView(APIView):
    def get(self, request, cid):
        '''
        获取商品详情
        :param request:
        :param cid: 商品id
        :return:
        '''
        if request.session.get('login'):
            commodity = Commodity.objects.filter(id=cid)
            if not commodity.exists():
                return JsonResponse({
                    'status': False,
                    'err': '找不到该内容'
                }, status=404)
            commodity = commodity[0]
            user = User_Info.objects.get(email=request.session.get('login'))
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
            CommodityViewLog.objects.create(
                ip=request.META['REMOTE_ADDR'],
                commodity=commodity,
                user=user
            )
            commodity.save()
            cmdResult = model_to_dict(commodity, exclude='status')
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
        修改商品内容
        :param request:
        :param cid:
        :return:
        '''
        if request.session.get('login'):
            params = request.body
            jsonParams = json.loads(params)
            try:
                commodity = Commodity.objects.filter(id=cid)
                if not commodity.exists():
                    return JsonResponse({
                        'status': False,
                        'err': '找不到该内容'
                    }, status=404)
                commodity = commodity[0]
                user = User_Info.objects.get(email=request.session.get('login'))
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
                        commodity.classification = Classification.objects.get(
                            name__exact=jsonParams.get('classification'))
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
                    'after_detail': commodity.c_detail,
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
                commodity = Commodity.objects.filter(id=cid)
                if not commodity.exists():
                    return JsonResponse({
                        'status': False,
                        'err': '找不到该内容'
                    }, status=404)
                commodity = commodity[0]
                user = User_Info.objects.get(email=request.session.get('login'))
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
            if jsonParams.get('name') == None or jsonParams.get('c_detail') == None or jsonParams.get(
                    'classification') == None:
                return JsonResponse({
                    'status': False,
                    'err': '输入错误'
                }, status=403)
            try:
                seller = User_Info.objects.get(email=request.session.get('login'))
                classification = Classification.objects.filter(name__exact=jsonParams.get('classification'))
                if not classification.exists():
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
