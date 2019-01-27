from apps.market.models import Commodity
from rest_framework.views import APIView
from django.http import JsonResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from ALGCommon.dictInfo import model_to_dict


class ListCommodity(APIView):
    EXCLUDE_FIELDS = [
        'comment', 'create_time', 'last_mod_time', 'status'
    ]

    def get(self, requests):
        '''
        获取商品列表
        :param requests:
        :return:
        '''
        try:
            page = requests.GET.get('page')
            commodityObj = Commodity.objects.all()
            commodityPage = Paginator(commodityObj, 5)

            try:
                commodityList = commodityPage.page(page)
            except PageNotAnInteger:
                commodityList = commodityPage.page(1)
            except EmptyPage:
                commodityList = commodityPage.page(1)

            commodity = [model_to_dict(mar, exclude=self.EXCLUDE_FIELDS) for mar in commodityList if
                         mar.status == 'p' or mar.status == 'o']

            return JsonResponse({
                'status': True,
                'commodityList': commodity,
                'has_previous': commodityList.has_previous(),
                'has_next': commodityList.has_next()
            })

        except:
            return JsonResponse({
                'status': False,
                'err': '出现未知的错误'
            }, status=403)