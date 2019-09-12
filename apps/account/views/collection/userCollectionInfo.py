from ALGCommon.userAuthCommon import check_login, getUser
from ALGCommon.dictInfo import model_to_dict
from ALGCommon.paginator import paginator
from rest_framework.views import APIView
from apps.market.models import CommodityCollection, Commodity
from apps.helps.models import ArticleCollection, Article
from django.http import JsonResponse


class UserCollectionInfoView(APIView):

    @check_login
    def get(self, request):
        '''
        获取本人收藏的商品
        :param request:
        :return:
        '''
        userID = getUser(request.session.get('login')).id
        page = request.GET.get('login')
        cclt = CommodityCollection.objects.filter(relatedUser=userID)
        ccltPage = paginator(cclt, page)
        cidList = [model_to_dict(c, fields='relatedCommodity') for c in ccltPage]
        for i in range(len(cidList)):
            cidList[i] = cidList[i]['relatedCommodity']


