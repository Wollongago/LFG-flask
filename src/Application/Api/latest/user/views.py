# import logging

# from Application.Api.latest.__schemas.user import UserSchema
# from Application.models import User
# from bson import ObjectId
# from Extensions import flask_pymongo
# from Extensions.Nestable.Classy import Classy42
# from Extensions.Nestable.flask_classy import route
# from flask import request
# from flask_bcrypt import check_password_hash, generate_password_hash

# # from Celery.tasks.steam import sync_user_profile (USED endpoint to test, since having import issues)

# __author__ = 'lonnstyle'
# from app import Application
# from flask import Flask, abort, flash, g, redirect, render_template, request, session, url_for
# from flask_openid import OpenID
# from models import User
# from openid.extensions import pape

# logger = logging.getLogger('Api')
# oid = OpenID(Application, safe_roots=[], extension_responses=[pape.Response])
#     #FIXME: fix routes
# login = "https://127.0.0.1:3000/signup"
# index = "https://127.0.0.1:3000/"
# class UserView(Classy42):
#     decorators = []
#     trailing_slash = False
#     route_base = '/'

#     @route('/')
#     def index():
#         if 'steam_id' not in session:
#             return redirect(url_for(login))
#         return redirect(url_for(index)) 
    
#     @route('/redirect', methods=['GET', 'POST'])
#     def steam_auth():
#         if 'steam_id' in session:
#             return redirect(url_for(index))
#         if request.method == 'POST':
#             steam_id = request.get_json('steam_id')
#             if steam_id:
#                 session['steam_id'] = steam_id
#                 pape_request = pape.Request([])
#                 return oid.try_login('https://steamcommunity.com/openid/login', 
#                                     ask_for =['steam_id', 'steam_name','steam_avatar','profileURL'],
#                                     extensions=pape_request)
#             return redirect(url_for(login), next = oid.get_next_url())
        
#     @route("/authorised")
#     def authorised(resp):
#         session['steam_id'] = resp.identity_url.split('/')[-1]
#         session['steam_name'] = resp.nickname
#         session['steam_avatar'] = resp.data.get('avatarfull')
#         session['profileURL'] = resp.profile
#         return redirect(url_for(index))

#     @route('/login', methods=['POST'])
#     def login_user(self):
#         # Load user input data
#         user_data = request.get_json()
#         # Validate user input data
#         user_schema = UserSchema()
#         errors = user_schema.validate(user_data)
#         if errors:
#             return errors, 400
#         # Check if user with given email exists
#         user = flask_pymongo.db.users.find_one({'email': user_data['email']})
#         print(user.__dict__)
#         if not user:
#             return {'error': 'User does not exist'}, 401
#         # Verify user's password
#         # if not check_password_hash(user.password, user_data['password']):
#         #     return 'Invalid password', 401
#         # User is authenticated, return success message
#         return 'User authenticated successfully!'

#     # USED this endpoint to test due to import issues
#     # @route('/steam', methods=['GET'])
#     # def steam_test(self):
#     #     return sync_user_profile()  
#     @route('/logout')
#     def logout():
#         session.pop('steam_id', None)
#         flash('You have been signed out')
#         return redirect(oid.get_next_url())
