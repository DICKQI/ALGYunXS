from apps.market.models import Commodity
from rest_framework.views import APIView
from django.http import JsonResponse
from ALGCommon.paginator import paginator
from ALGCommon.dictInfo import model_to_dict


class ListCommodity(APIView):
    EXCLUDE_FIELDS = [
        'comment', 'create_time', 'last_mod_time', 'status', 'commodity_img', 'detail'
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
            commodityList = paginator(commodityObj, page)

            commodity = [model_to_dict(mar, exclude=self.EXCLUDE_FIELDS) for mar in commodityList if
                         mar.status == 'p' or mar.status == 'o']
            i = 0
            for com in commodity:
                if commodityList[i].commodity_img.first():
                    com['commodity_img'] = 'https://algyunxs.oss-cn-shenzhen.aliyuncs.com/media/' + commodityList[
                        i].commodity_img.first().img.name + '?x-oss-process=style/head_portrait'
                else:
                    com['commodity_img'] = None
                com['detail'] = commodityList[i].detail[:30]
                i += 1

            return JsonResponse({
                'status': True,
                'commodityList': commodity,
                'has_previous': commodityList.has_previous(),
                'has_next': commodityList.has_next(),
            })

        except:
            return JsonResponse({
                'status': False,
                'err': '出现未知的错误'
            }, status=403)
