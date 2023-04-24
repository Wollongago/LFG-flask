from flask import request, jsonify
from flask_bcrypt import generate_password_hash, check_password_hash
from Extensions.Nestable import NestableBlueprint
from models import User
from .schema.user import UserSchema


__author__ = 'KycKyc'
collection = NestableBlueprint("Application", __name__)
collection.register_collection(__file__)

@collection.route('/register', methods=['POST'])
def register_user():
    # Load user input data
    user_data = request.get_json()
    # Validate user input data
    user_schema = UserSchema()
    errors = user_schema.validate(user_data)
    if errors:
        return jsonify(errors), 400
    # Check if user with given email exists
    existing_user = User.find_one({'email': user_data['email']})
    if existing_user:
        return 'User already exists', 409
    # Create new user object
    user = User(
        email=user_data['email'],
        password=generate_password_hash(user_data['password']).decode('utf-8')
    )
    # Save new user to database
    user.save(user)

    

    # Return success message
    return 'User registered successfully!'

@collection.route('/login', methods=['POST'])
def login_user():
    # Load user input data
    user_data = request.get_json()
    # Validate user input data
    user_schema = UserSchema()
    errors = user_schema.validate(user_data)
    if errors:
        return jsonify(errors), 400
    # Check if user with given email exists
    user = User.find_one({'email': user_data['email']})
    print(user.__dict__)
    if not user:
        return 'User not found', 401
    # Verify user's password
    # if not check_password_hash(user.password, user_data['password']):
    #     return 'Invalid password', 401
    # User is authenticated, return success message
    return 'User authenticated successfully!'
