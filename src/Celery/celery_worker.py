from __future__ import absolute_import

from pprint import pformat, pprint

from app import Application
from Celery import celery_tasks

print('{:=^50}'.format('Celery worker'))
celery_app = Application(launch_mode='celery')()
print()