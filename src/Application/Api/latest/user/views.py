import logging

from Application.Api.latest.__schemas.user import User as UserDump
from Application.models import User
from bson import ObjectId
from Extensions import flask_pymongo
from Extensions.Nestable.Classy import Classy42
from Extensions.Nestable.flask_classy import route
from flask import request

__author__ = 'lonnstyle'

logger = logging.getLogger('Api')

class ProfileView(Classy42):
    decorators = []
    trailing_slash = False
    route_base = '/profile/<user_id>'

    def index(self, user_id):
        if not ObjectId.is_valid(user_id):
            return {'error': 'Invalid ObjectId'}
        user = User.find_one({'_id': ObjectId(user_id)})
        if user is not None:
            return {'payload':
                    {'profile': UserDump().dump(user._data)}
                    }
        return {'error': 'User not found'}