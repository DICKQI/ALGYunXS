from apps.market.models import CommodityImage, Commodity
from rest_framework.views import APIView
from ALGCommon.userAuthCommon import check_login
from django.http import JsonResponse
import oss2


class CImgView(APIView):
    @check_login
    def post(self, request, cid):
        '''
        更新商品图片
        :param request:
        :param cid:
        :return:
        '''
        try:
            commodity = Commodity.objects.get(id=cid)
            if commodity.commodity_img.count() > 5:
                return JsonResponse({
                    'status': False,
                    'err': '已超出图片上限(最多5张照片)'
                }, status=401)
            get_img = request.FILES.get('img')
            img = CommodityImage.objects.create(img=get_img)
            commodity.commodity_img.add(img)
            commodity.save()
            return JsonResponse({
                'status': True,
                'result': img.id
            })
        except:
            return JsonResponse({
                'status': False,
                'err': '意料以外的错误'
            }, status=403)

    @check_login
    def delete(self, request, cid, mid):
        '''
        给文章移除图片
        :param request:
        :param cid:
        :param mid:
        :return:
        '''
        commodity = Commodity.objects.filter(id=cid)
        if not commodity.exists():
            return JsonResponse({
                'status': False,
                'err': '商品不存在'
            }, status=403)
        img = CommodityImage.objects.filter(id=mid)
        if not img.exists():
            return JsonResponse({
                'status': False,
                'err': '图片不存在'
            }, status=403)
        try:
            commodity.commodity_img.remove(img)
            '''删除oss文件'''
            object_name = 'media/' + str(img)
            auth = oss2.Auth('LTAIpK0JtS9hsWkG', 'cQpsrRs3Nhv6hTRpEMuUA2pjX6BlWs')
            bucket = oss2.Bucket(auth, 'oss-cn-shenzhen.aliyuncs.com', 'algyunxs')
            bucket.delete_object(object_name)
            '''同时删除数据库表的内容'''
            img.delete()
        except:
            return JsonResponse({
                'status': False,
                'err': '删除失败'
            }, status=403)
        return JsonResponse({
            'status': True,
            'result': '删除成功'
        })