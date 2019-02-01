from apps.log.models import CommodityViewLog, HelpsViewLog
from apps.account.models import User_Info
from django.http import JsonResponse
from rest_framework.views import APIView
from ALGCommon.dictInfo import model_to_dict


class UserLogView(APIView):
    COMMODITY_INCLUDE_FIELDS = [
        'id', 'name'
    ]

    def get(self, request):
        '''
        获取当前用户的浏览记录
        :param request:
        :return:
        '''
        if request.session.get('login'):
            try:
                user = User_Info.objects.get(phone_number__exact=request.session.get('login'))
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
        else:
            return JsonResponse({
                'status': False,
                'err': '你还没登录'
            }, status=401)
