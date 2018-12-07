from apps.market.models import CommodityImage, Commodity
from rest_framework.views import APIView
from django.http import JsonResponse


class CImgView(APIView):
    def put(self, request, cid):
        '''
        更新商品图片
        :param request:
        :param cid:
        :return:
        '''
        if request.session.get('login') != None:

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
                    'result':img.id
                })
            except:
                return JsonResponse({
                    'status':False,
                    'err': '意料以外的错误'
                }, status=403)
        else:
            return JsonResponse({
                'status':False,
                'err': '你还未登录'
            }, status=401)