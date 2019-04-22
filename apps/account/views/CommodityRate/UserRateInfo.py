from rest_framework.views import APIView
from apps.market.models import BuyerRateModel
from apps.account.models import User_Info
from ALGCommon.paginator import paginator
from ALGCommon.dictInfo import model_to_dict
from ALGCommon.userAuthCommon import check_login
from django.http import JsonResponse


class RateInfoView(APIView):

    @check_login
    def get(self, request, uid):
        '''
        获取用户评价信息
        :param request:
        :param uid:
        :return:
        '''
        user = User_Info.objects.filter(id=uid)
        if not user.exists():
            return JsonResponse({
                'status': False,
                'err': '用户不存在'
            }, status=403)
        user = user[0]
        rates = BuyerRateModel.objects.filter(
            relatedOrder__commodity__seller=user
        )
        page = request.GET.get('page')
        rateList = paginator(rates, page)
        return JsonResponse({
            'status': True,
            'rates': [model_to_dict(rate) for rate in rateList],
            'has_next': rateList.has_next(),
            'has_previous': rateList.has_previous()
        })
