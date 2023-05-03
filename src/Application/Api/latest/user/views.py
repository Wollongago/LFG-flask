import logging

from flask_bcrypt import generate_password_hash, check_password_hash

from models import User
from src.Application.Api.latest.__schemas.user import UserSchema
from bson import ObjectId
from Extensions import flask_pymongo
from Extensions.Nestable.Classy import Classy42
from Extensions.Nestable.flask_classy import route
from flask import request


__author__ = 'lonnstyle'

logger = logging.getLogger('Api')

class UserView(Classy42):
    decorators = []
    trailing_slash = False
    route_base = '/'

    def index(self):
        return {}

    @route('/register', methods=['POST'])
    def register_user(self):
        # Load user input data
        user_data = request.get_json()
        # Validate user input data
        user_schema = UserSchema()
        errors = user_schema.validate(user_data)
        if errors:
            return {'error': errors}, 400
        # Check if user with given email exists
        existing_user = User.find_one({'email': user_data['email']})
        if existing_user:
            return { "error": "User already exists" }, 400
        # Create new user object
        user = User(
            email=user_data['email'],
            password=generate_password_hash(user_data['password']).decode('utf-8')
        )
        # Save new user to database
        user.save(user)

        # Return success message
        return 'User registered successfully!'

    @route('/login', methods=['POST'])
    def login_user(self):
        # Load user input data
        user_data = request.get_json()
        # Validate user input data
        user_schema = UserSchema()
        errors = user_schema.validate(user_data)
        if errors:
            return errors, 400
        # Check if user with given email exists
        user = User.find_one({'email': user_data['email']})
        print(user.__dict__)
        if not user:
            return {'error': 'User does not exist'}, 401
        # Verify user's password
        # if not check_password_hash(user.password, user_data['password']):
        #     return 'Invalid password', 401
        # User is authenticated, return success message
        return 'User authenticated successfully!'
