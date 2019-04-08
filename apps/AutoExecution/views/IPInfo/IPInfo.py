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
        logs = VisitLog.objects.all()
        for log in logs:
            if not log.lock:
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
        logs = VisitLog.objects.all()
        for log in logs:
            if log.lock:
                log.lock = False
                log.five_min_visit = 0
                log.save()
        return HttpResponse('回家吧')

