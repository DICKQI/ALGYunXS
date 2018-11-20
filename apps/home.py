from rest_framework.views import APIView
from django.http import JsonResponse
from django.shortcuts import Http404
import json
class HomeIndex(APIView):
    def get(self, requests):
        html = '欢迎来到ALGYun'
        return JsonResponse({'html':html})
    def post(self, requests):
        # params = requests.body
#         # try:
#         #     data = json.loads(params)
#         #     html = '欢迎' + data['postman'] + '来到ALGYun'
#         #     return JsonResponse({
#         #         'html':html
#         #     })
#         # except:
#         #     return JsonResponse({'err':'输入错误'})
        params = requests.POST.get(
            'postman'
        )
        html = '欢迎' + str(params) + '来到ALGYun'
        return JsonResponse({'html':html})