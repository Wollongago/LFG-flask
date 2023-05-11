import os

from celery import Celery
from Celery.celery_worker import celery_app
from celery.schedules import crontab

from Celery.tasks.steam import get_user_profile


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    print('setup_periodic_tasks')
    print(sender)

celery_app.add_periodic_task(30.0, get_user_profile()) #use crontab scheduler, make the synchronization functions in the parser file

