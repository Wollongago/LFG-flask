import json
import time
from pprint import pformat, pprint

import Celery.celery_scheduler
# from Celery.tasks import ()
# add the import when have tasks in the folder
from Extensions import celery_app, flask_pymongo

print("Registered Tasks:",pformat(celery_app.tasks))
