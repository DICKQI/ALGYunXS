from rest_framework.views import APIView
from django.http import JsonResponse, HttpResponse
import json

class TestView(APIView):

    def post(self, requests):
        postBody = requests.body
        jsonData = json.loads(postBody)
        return JsonResponse(jsonData)
