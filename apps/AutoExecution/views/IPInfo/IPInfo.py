from apps.log.models import VisitLog
from rest_framework.views import APIView
from django.http import HttpResponse
import time


class IPInfoView(APIView):

    def get(self, request):
        '''
        自动重置ip5分钟访问次数
        :param request:
        :return:
        '''
        begin = time.time()
        logs = VisitLog.objects.filter(lock=False)
        for log in logs:
            log.five_min_visit = 0
            log.save()
        end = time.time()

        return HttpResponse(end - begin)

    def delete(self, request):
        '''
        解锁IP
        :param request:
        :return:
        '''
        begin = time.time()
        logs = VisitLog.objects.filter(lock=True)
        for log in logs:
            log.lock = False
            log.five_min_visit = 0
            log.save()
        end = time.time()
        return HttpResponse(end - begin)

