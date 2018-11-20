from rest_framework.views import APIView
from django.http import JsonResponse
from django.shortcuts import Http404
import json
class HomeIndex(APIView):
    def get(self, request):
        html = '欢迎来到ALGYun'
        return JsonResponse({'html':html})
    def post(self, request):
        params = request.body
        try:
            data = json.loads(params)
            html = '欢迎' + data['postman'] + '来到ALGYun'
            return JsonResponse({
                'html':html
            })
        except:
            return JsonResponse({'err':'输入错误'})