from rest_framework.views import APIView
from django.http import JsonResponse
import json
class HomeIndex(APIView):
    def get(self, requests):
        html = '欢迎来到ALGYun'
        return JsonResponse({'html':html})
    def post(self, requests):
        params = requests.body
        data = json.loads(params)
        html = '欢迎' + data['postman'] + '来到ALGYun'
        password = data['password']
        return JsonResponse({
            'html':html,
            'password':password
        })