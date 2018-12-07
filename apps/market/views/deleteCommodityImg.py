from rest_framework.views import APIView
from django.http import JsonResponse
from apps.market.models import CommodityImage, Commodity
import oss2
class DeleteImage(APIView):
    def delete(self, request, cid, mid):
        '''
        给文章移除图片
        :param request:
        :param cid:
        :param mid:
        :return:
        '''
        if request.session.get('login'):
            try:
                commodity = Commodity.objects.get(id=cid)
            except:
                return JsonResponse({
                    'status':False,
                    'err': '商品不存在'
                }, status=403)
            try:
                img = CommodityImage.objects.get(id=mid)
            except:
                return JsonResponse({
                    'status':False,
                    'err': '图片不存在'
                }, status=403)
            try:
                commodity.commodity_img.remove(img)
            except:
                return JsonResponse({
                    'status':False,
                    'err': '删除失败'
                }, status=403)
            commodity.save()
            try:
                '''删除oss文件'''
                object_name = 'media/' + str(img)
                auth = oss2.Auth('LTAIpK0JtS9hsWkG', 'cQpsrRs3Nhv6hTRpEMuUA2pjX6BlWs')
                bucket = oss2.Bucket(auth, 'oss-cn-shenzhen.aliyuncs.com', 'algyunxs')
                bucket.delete_object(object_name)
                img.delete()
            except:
                return JsonResponse({
                    'status':False,
                    'err': '删除失败'
                }, status=403)
            return JsonResponse({
                'status':True,
                'result':'删除成功'
            })
        else:
            return JsonResponse({
                'status':False,
                'err': '你还没登录呢'
            }, status=401)