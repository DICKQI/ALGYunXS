from rest_framework.views import APIView
from django.http import JsonResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from ALGCommon.dictInfo import model_to_dict
from apps.helps.models import Article


class ListHelps(APIView):
    EXCLUDE_FIELDS = [
        'comment', 'create_time', 'status'
    ]

    def get(self, requests):
        '''
        获取互帮互助文章列表
        :param requests:
        :return:
        '''
        try:
            page = requests.GET.get('page')
            articleObj = Article.objects.all()
            articlePage = Paginator(articleObj, 5)
            try:
                articleList = articlePage.page(page)
            except PageNotAnInteger:
                articleList = articlePage.page(1)
            except EmptyPage:
                articleList = articlePage.page(1)

            article = [model_to_dict(art, exclude=self.EXCLUDE_FIELDS) for art in articleList if art.status == 'p']

            return JsonResponse({
                'status': True,
                'articleList': article,
                'has_previous': articleList.has_previous(),
                'has_next': articleList.has_next()
            })
        except:
            return JsonResponse({
                'status': False,
                'err': '出现未知的错误'
            }, status=403)