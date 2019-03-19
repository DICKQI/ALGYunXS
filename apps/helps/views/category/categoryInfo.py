from rest_framework.views import APIView
from apps.helps.models import Category
from ALGCommon.dictInfo import model_to_dict
from ALGCommon.userCheck import check_login, authCheck
from django.http import JsonResponse
import json


class CategoryView(APIView):

    @check_login
    def get(self, request):
        '''
        获取文章分类列表
        :param request:
        :return:
        '''
        categoryAll = Category.objects.all()
        result = [model_to_dict(category) for category in categoryAll]
        return JsonResponse({
            'status': True,
            'category': result
        })

    @check_login
    def post(self, request):
        '''
        新增文章分裂
        :param request:
        :return:
        '''
        try:
            if not authCheck(['12', '515400'], request.session.get('login')):
                return JsonResponse({
                    'err': '你没有权限',
                    'status': False
                }, status=401)
            params = json.loads(request.body)
            if Category.objects.filter(name=params.get('name')).exists():
                return JsonResponse({
                    'status': False,
                    'err': '分类名已存在'
                }, status=401)
            category = Category.objects.create(name=params.get('name'))
            return JsonResponse({
                'status': True,
                'id': category.id
            })
        except:
            return JsonResponse({
                'status': False,
                'err': '出现未知错误'
            }, status=403)