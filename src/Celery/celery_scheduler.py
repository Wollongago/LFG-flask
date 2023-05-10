import os

from celery import Celery
from Celery.celery_worker import celery_app
from celery.schedules import crontab

from Celery.tasks import steam


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    print('setup_periodic_tasks')
    print(sender)

celery_app.add_periodic_task()

