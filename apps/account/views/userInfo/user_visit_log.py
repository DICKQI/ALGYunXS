from apps.log.models import CommodityViewLog, HelpsViewLog
from apps.account.models import User_Info
from django.http import JsonResponse
from rest_framework.views import APIView
from ALGCommon.dictInfo import model_to_dict
from ALGCommon.check_login import check_login


class UserLogView(APIView):
    COMMODITY_INCLUDE_FIELDS = [
        'id', 'name'
    ]

    @check_login
    def get(self, request):
        '''
        获取当前用户的浏览记录(商品和帮助消息)
        :param request:
        :return:
        '''
        try:
            user = User_Info.objects.get(email__exact=request.session.get('login'))
            commodityLog = CommodityViewLog.objects.filter(user=user)
            helpsLog = HelpsViewLog.objects.filter(user=user)

            commodityList = [commodity.commodity for commodity in commodityLog]
            helpsList = [helps.HelpsArticle for helps in helpsLog]

            commodityResult = [model_to_dict(commodity, fields=self.COMMODITY_INCLUDE_FIELDS) for commodity in
                               commodityList]
            helpsResult = [model_to_dict(helps) for helps in helpsList]

            return JsonResponse({
                'status': True,
                'commodity': commodityResult,
                'helps': helpsResult
            })
        except:
            return JsonResponse({
                'status': False,
                'err': '意料之外的错误'
            }, status=403)
