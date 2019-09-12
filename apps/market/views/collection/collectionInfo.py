from ALGCommon.userAuthCommon import check_login, getUser
from ALGCommon.dictInfo import model_to_dict
from ALGCommon.paginator import paginator
from rest_framework.views import APIView
from apps.market.models import CommodityCollection, Commodity
from django.http import JsonResponse


class CommodityCollectionInfoView(APIView):

    @check_login
    def post(self, request, cid):
        '''
        收藏商品
        :param request:
        :return:
        '''
        myselfID = getUser(request.session.get('login')).id
        commodity = Commodity.objects.filter(id=cid)
        if not commodity.exists():
            return JsonResponse({
                'status': False,
                'err': '商品不存在'
            }, status=404)
        # 创建收藏数据表
        cclt = CommodityCollection.objects.create(
            relatedUser=myselfID,
            relatedCommodity=cid
        )
        return JsonResponse({
            'status': True,
            'collection_id': cclt.id
        })

