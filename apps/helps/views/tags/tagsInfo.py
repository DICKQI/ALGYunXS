from apps.helps.models import Tag, Article
from rest_framework.views import APIView
from ALGCommon.dictInfo import model_to_dict
from ALGCommon.userAuthCommon import check_login
from ALGCommon.paginator import paginator
from django.http import JsonResponse



class TagsInfoView(APIView):
    EXCLUDE_FIELDS = [
        'comment', 'create_time', 'status', 'tags'
    ]

    @check_login
    def get(self, request, tid):
        '''
        根据标签获取文章
        :param request:
        :param tid:
        :return:
        '''
        try:
            page = request.GET.get('page')
            tag = Tag.objects.filter(id=tid)
            if not tag.exists():
                return JsonResponse({
                    'status': False,
                    'err': '标签不存在',
                }, status=404)
            tag = tag[0]
            article = Article.objects.filter(tags=tag)
            articleList = paginator(article, page)
            result = [model_to_dict(art, exclude=self.EXCLUDE_FIELDS) for art in articleList if art.status == 'p']
            return JsonResponse({
                'status': True,
                'article': result
            })
        except:
            return JsonResponse({
                'status': False,
                'err': '出现未知错误'
            }, status=403)
