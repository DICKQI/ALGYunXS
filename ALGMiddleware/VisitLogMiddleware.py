from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from django.utils.timezone import now
from apps.log.models import VisitLog, IpVisitTime
from threading import Timer

class VisitLogFirewall(MiddlewareMixin):

    def process_request(self, request):
        try:
            visitLog = VisitLog.objects.get(ip=request.META['REMOTE_ADDR'])
            visitLog.visit_count += 1
            time = IpVisitTime.objects.create(time=now())
            visitLog.time.add(time)
            if visitLog.lock:
                visitLog.save()
                return JsonResponse({
                    'status':False,
                    'err':'访问过于频繁，请稍后再试'
                }, status=403)
            visitLog.five_min_visit += 1
            if visitLog.five_min_visit >= 300:
                visitLog.lock = True
                Timer(300, unlockIP, [str(request.META['REMOTE_ADDR'])]).start()
            visitLog.save()
            return None
        except:
            visitLog = VisitLog.objects.create(ip=request.META['REMOTE_ADDR'])

            time = IpVisitTime.objects.create(time=now())

            visitLog.time.add(time)

            visitLog.save()

            return None

def unlockIP(ip):
    log = VisitLog.objects.get(ip=ip)
    log.lock = False
    log.five_min_visit = 0
    log.save()
