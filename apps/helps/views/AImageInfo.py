from rest_framework.views import APIView
from django.http import JsonResponse
from ALGCommon.check_login import check_login
from apps.helps.models import Article

class ImageView(APIView):

    @check_login
    def post(self, request, aid):
        '''
        为文章添加或修改附图
        :param request:
        :param aid:
        :return:
        '''
        try:
            article = Article.objects.filter(id=aid)
            if not article.exists():
                return JsonResponse({
                    'status': False,
                    'err': '文章不存在'
                }, status=404)
            article = article[0]
            article.img = request.FILES.get('img')
            article.save()
            return JsonResponse({
                'status': True,
                'id': aid
            })
        except:
            return JsonResponse({
                'status': False,
                'err': '失败'
            }, status=403)