from rest_framework.views import APIView
from apps.helps.models import Article, HelpsStarRecord
from apps.account.models import User_Info
from django.http import JsonResponse
from django.db.models import Q
from ALGCommon.check_login import check_login



class StarInfoView(APIView):

    @check_login
    def get(self, request, aid):
        '''
        为文章点赞
        :param request:
        :param aid:
        :return:
        '''
        article = Article.objects.filter(id=aid)
        if not article.exists():
            return JsonResponse({
                'status': False,
                'err': '文章不存在'
            }, status=404)
        article = article[0]

        if HelpsStarRecord.objects.filter(
                Q(article=article) & Q(star_man=User_Info.objects.get(email=request.session.get('login')))
        ).exists():
            return JsonResponse({
                'status': False,
                'err': '不能重复点赞噢'
            }, status=401)
        article.stars += 1
        article.save()
        HelpsStarRecord.objects.create(
            star_man=User_Info.objects.get(email=request.session.get('login')),
            article=article
        )
        return JsonResponse({
            'status': True,
            'id': aid
        })

