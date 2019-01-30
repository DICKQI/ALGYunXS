import uwsgi
from .script.AutoResetIPCount import *

for job_id, job in enumerate(jobs):
    uwsgi.register_sinal(job_id, '', jobs['name'])
    if len(job['time']) == 1:
        uwsgi.add_timer(job_id, job['time'][0])
    else:
        uwsgi.add_cron(job_id, job['time'][0], job['time'][1], job['time'][2], job['time'][3], job['time'][4])