from rest_framework.views import APIView
from django.http import JsonResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from ALGPackage.dictInfo import model_to_dict
from apps.account.models import User_Info
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
        首页
        :param request:
        :return:
        '''
        try:
            user = User_Info.objects.get(username=request.session.get('login'))
            id = {'id': user.id, 'nickname': user.nickname, 'head_portrait':'https://algyunxs.oss-cn-shenzhen.aliyuncs.com/media/' + str(user.head_portrait) + '?x-oss-process=style/head_portrait'}
        except:
            id = {'err': '未登录'}
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
        marResult = [model_to_dict(mar, exclude=self.EXCLUDE_FIELDS) for mar in marList if mar.status == 'p'  or mar.status == 'o']
        ptjResult = [model_to_dict(ptj, exclude=self.EXCLUDE_FIELDS) for ptj in ptjList]

        return JsonResponse({'result': {
            'helps': artResult,
            'markets': marResult,
            'part_time_job': ptjResult,
            'notice': noticeResult,
            'id': id,
            'A_has_previous': artList.has_previous(),
            'M_has_previous': marList.has_previous(),
            'P_has_previous': ptjList.has_previous(),
            'A_has_next': artList.has_next(),
            'M_has_next': marList.has_next(),
            'P_has_next': ptjList.has_next()
        }})
