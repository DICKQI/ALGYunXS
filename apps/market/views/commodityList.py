from apps.market.models import Commodity, Classification
from rest_framework.views import APIView
from django.http import JsonResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
