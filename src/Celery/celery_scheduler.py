import os

from celery import Celery
from Celery.celery_worker import celery_app
from celery.schedules import crontab

# from Celery.tasks import ()
# add the import when have tasks in the folder  



@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    print('setup_periodic_tasks')
    print(sender)