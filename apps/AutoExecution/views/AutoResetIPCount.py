from apps.log.models import VisitLog
from threading import Timer

# Create your views here.
'''
    这个脚本用来重置所有ip的单位时间内访问次数
    每5分钟重置一次
'''

def reset():
    try:
        logs = VisitLog.objects.all()
        for log in logs:
            if log.lock == False:
                log.five_min_visit = 0
                log.save()
        global timer
        timer = Timer(300, reset).start()
        print('reset count complete')
    except:
        return
reset()
