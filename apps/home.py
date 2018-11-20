from rest_framework.views import APIView
from django.http import JsonResponse

class HomeIndex(APIView):
    def get(self, request):
        html = '欢迎来到ALGYun'
        return JsonResponse({'html':html})
    def post(self, request):
        params = request.POST
        try:
            html = '欢迎' + params.get('postman') + '来到ALGYun'
            return JsonResponse({'result':html})
        except:
            return JsonResponse({'err': '输入错误'})