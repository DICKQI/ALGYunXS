from rest_framework.views import APIView
from django.http import JsonResponse
from ALGCommon.dictInfo import model_to_dict
from apps.helps.models import Article
from apps.account.models import User_Info
from apps.log.models import HelpsViewLog

class HelpsInfoView(APIView):
    def get(self, request, pid):
        '''
        获取互帮互助信息详情
        :param request:
        :param pid:
        :return:
        '''
        if request.session.get('login'):
            article = Article.objects.filter(id=pid)
            if not article.exists():
                return JsonResponse({
                    'status': False,
                    'err': '找不到该内容'
                }, status=404)
            article = article[0]
            user = User_Info.objects.get(email__exact=request.session.get('login'))
            if user != article.author:
                if article.status == 's':
                    # 未发布的文章非作者无法直接查看
                    return JsonResponse({
                        'status': False,
                        'err': '找不到该内容'
                    }, status=404)
            article.views += 1
            HelpsViewLog.objects.create(
                ip=request.META['REMOTE_ADDR'],
                user=user,
                HelpsArticle=article
            )
            return JsonResponse({
                'status':True,
                'article':model_to_dict(article)
            })
        else:
            return JsonResponse({
                'status': False,
                'err': '你还未登录'
            }, status=401)
