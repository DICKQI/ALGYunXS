from rest_framework.views import APIView
from django.http import JsonResponse
from ALGCommon.userAuthCommon import check_login
from apps.helps.models import Article
import oss2

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
            if article.img:
                # 如果文章已有配图
                # 删除oss存储的文件
                object_name = 'media/' + str(article.img.name)
                auth = oss2.Auth('LTAIpK0JtS9hsWkG', 'cQpsrRs3Nhv6hTRpEMuUA2pjX6BlWs')
                bucket = oss2.Bucket(auth, 'oss-cn-shenzhen.aliyuncs.com', 'algyunxs')
                bucket.delete_object(object_name)
                article.img.delete()
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