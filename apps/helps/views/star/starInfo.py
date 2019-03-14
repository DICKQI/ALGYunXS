from rest_framework.views import APIView
from apps.helps.models import Article, HelpsStarRecord
from apps.account.models import User_Info
from django.http import JsonResponse
from django.db.models import Q
from ALGCommon.userCheck import check_login



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
        HelpsStarRecord.objects.create(
            star_man=User_Info.objects.get(email=request.session.get('login')),
            article=article
        )
        article.save()
        return JsonResponse({
            'status': True,
            'id': aid
        })

    @check_login
    def delete(self, request, aid):
        '''
        取消文章的点赞
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
        record = HelpsStarRecord.objects.filter(
                Q(article=article) & Q(star_man=User_Info.objects.get(email=request.session.get('login')))
        )
        if not record.exists():
            return JsonResponse({
                'status': False,
                'err': '你还没对其点赞'
            }, status=401)
        record = record[0]
        article.stars -= 1
        record.delete()
        article.save()
        return JsonResponse({
            'status': True,
            'id': aid
        })

