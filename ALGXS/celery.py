import os
from celery import Celery, platforms
from celery.schedules import crontab
from datetime import timedelta



# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website.settings')

app = Celery('ALGYunXS')

# Using a string here means the worker don't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')


# 防止内存泄漏，设置最大任务个数
CELERYD_MAX_TASKS_PER_CHILD = 10

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


# celery 定时任务配置
# app.conf.update(
#     CELERYBEAT_SCHEDULE = {
#         'test': {
#             'task': 'apps.AutoExecution.views.Recalculation_of_credit_scores.recalculation',
#             'schedule': timedelta(seconds=1)
#         }
#     }
# )

# 允许root 用户运行celery
platforms.C_FORCE_ROOT = True

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
