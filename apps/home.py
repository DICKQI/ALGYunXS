from rest_framework.views import APIView
from django.http import JsonResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from ALGPackage.dictInfo import model_to_dict
from apps.market.models import Commodity
from apps.helps.models import Article
from apps.PTJ.models import PTJInfo
from apps.FandQ.models import Notice


class HomeIndex(APIView):
    EXCLUDE_FIELDS = [
        'comment', 'create_time', 'last_mod_time'
    ]

    def get(self, request):
        '''
        获取helps markets
        :param request:
        :return:
        '''
        try:
            try:
                notice = Notice.objects.all()
                noticeResult = model_to_dict(notice.first(), exclude='id')
            except:
                noticeResult = {}
            apage = request.GET.get('apage')
            mpage = request.GET.get('mpage')
            ppage = request.GET.get('ppage')
            articles = Article.objects.all()
            artPage = Paginator(articles, 5)
            markets = Commodity.objects.all()
            marPage = Paginator(markets, 5)
            ptjInfo = PTJInfo.objects.all()
            ptjPage = Paginator(ptjInfo, 5)

            try:
                artList = artPage.page(apage)
            except PageNotAnInteger:
                artList = artPage.page(1)
            except EmptyPage:
                artList = artPage.page(artPage.num_pages)
            try:
                marList = marPage.page(mpage)
            except PageNotAnInteger:
                marList = marPage.page(1)
            except EmptyPage:
                marList = marPage.page(marPage.num_pages)
            try:
                ptjList = ptjPage.page(ppage)
            except PageNotAnInteger:
                ptjList = ptjPage.page(1)
            except EmptyPage:
                ptjList = ptjPage.page(ptjPage.num_pages)

            artResult = [model_to_dict(art, exclude=self.EXCLUDE_FIELDS) for art in artList if art.status == 'p']
            marResult = [model_to_dict(mar, exclude=self.EXCLUDE_FIELDS) for mar in marList if mar.status == 'p' or mar.status == 'o']
            ptjResult = [model_to_dict(ptj, exclude=self.EXCLUDE_FIELDS) for ptj in ptjList]

            return JsonResponse({'result': {
                'status':True,
                'helps': artResult,
                'markets': marResult,
                'part_time_job': ptjResult,
                'notice': noticeResult,
                'A_has_previous': artList.has_previous(),
                'M_has_previous': marList.has_previous(),
                'P_has_previous': ptjList.has_previous(),
                'A_has_next': artList.has_next(),
                'M_has_next': marList.has_next(),
                'P_has_next': ptjList.has_next()
            }})
        except:
            return JsonResponse({
                'status':False,
                'err':'出现未知的错误'
            }, status=403)
