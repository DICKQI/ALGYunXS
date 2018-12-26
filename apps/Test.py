from rest_framework.views import APIView
from django.http import JsonResponse, HttpResponse
import json

class TestView(APIView):

    def post(self, requests):
        try:
            postBody = requests.body
            jsonData = json.loads(postBody)
            return JsonResponse(jsonData)
        except:
            return JsonResponse({
                'err':'错误'
            })