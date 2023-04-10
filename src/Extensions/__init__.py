from celery import Celery

celery_app = Celery(__name__)
from flask_marshmallow import Marshmallow
from flask_pymongo import PyMongo

flask_pymongo = PyMongo()
marshmallow = Marshmallow()
