from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from apps.log.models import BlackList

class IPFirewall(MiddlewareMixin):
    def process_request(self, request):
        try:
            BlackList.objects.get(ip=request.META['REMOTE_ADDR'])
            return JsonResponse({
                'status':False,
                'err':'FORBIDDEN IP'
            }, status=403)
        except:
            return None
