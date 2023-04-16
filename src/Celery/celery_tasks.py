import json
import time
from pprint import pformat, pprint

# from Celery.tasks import ()
# add the import when have tasks in the folder
from Extensions import celery_app, flask_pymongo

print("Registered Tasks:",pformat(celery_app.tasks))
