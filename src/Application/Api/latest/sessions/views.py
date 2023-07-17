import datetime
import logging

from bson import ObjectId
from Extensions import flask_pymongo
from Extensions.Nestable.Classy import Classy42
from Extensions.Nestable.flask_classy import route
from flask import request

from .schemas import Session, SessionDump

__author__ = 'lonnstyle'

logger = logging.getLogger('Api')


class SessionView(Classy42):
    decorators = []
    trailing_slash = False
    route_base = '/'

    def index(self):
        '''
        index return all sessions
        '''
        sessions = flask_pymongo.db.sessions.find()
        schema = SessionDump()
        sessions = schema.dump_many(sessions)
        # TODO:dump sessions into a list of session
        return {'payload':{
            'sessions': sessions
        }}
    

    @route('/<session_id>', methods=['GET'])
    def get(self, session_id):
        if not ObjectId.is_valid(session_id):
            return {'error': 'Invalid session ObjectId'}
        session = flask_pymongo.db.sessions.find_one({'_id': ObjectId(session_id)})
        if not session:
            return {'error': 'Invalid session ObjectId'}
        schema = SessionDump()
        session = schema.dump(session)
        return {'payload': {
            'session': session
        }}

    @route('/', methods=['POST'])
    def post(self):
        args = request.get_json()
        schema = Session()
        data = schema.load(args).data
        return {'payload': {
            'session': data
        }}

    @route('/<session_id>', methods=['PUT'])
    def put(self, session_id):
        args = request.get_json()
        if any(key != 'userJoin' for key in args.keys()):
            return {'error': 'Invalid request, only userJoin is allowed'}
        user = args['userJoin']
        if len(user) != 1:
            return {'error': 'Invalid request, only one user is allowed to join'}
        user_id = user[0]
        if not ObjectId.is_valid(user_id):
            return {'error': 'Invalid user ObjectId'}
        user = flask_pymongo.db.users.find_one({'_id': ObjectId(user_id)})
        if not user:
            return {'error': 'Invalid user ObjectId'}
        if not ObjectId.is_valid(session_id):
            return {'error': 'Invalid session ObjectId'}
        session = flask_pymongo.db.sessions.find_one({'_id': ObjectId(session_id)})
        if not session:
            return {'error': 'Invalid session ObjectId'}
        if len(session['joinedUserIds']) >= session['partyCapacity']:
            return {'error': 'Session is full'}
        if user in session['joinedUserIds']:
            return {'error': 'User already joined the session'}
        flask_pymongo.db.sessions.update_one({'_id': ObjectId(session_id)}, {'$push': {'joinedUserIds': user}})
        session = flask_pymongo.db.sessions.find_one({'_id': ObjectId(session_id)})        
        return {'payload': {
            'session': session
        }}

    @route('/<session_id>', methods=['DELETE'])
    def delete(self, session_id):
        if not ObjectId.is_valid(session_id):
            return {'error': 'Invalid session ObjectId'}
        cnt = flask_pymongo.db.sessions.delete_one({'_id': ObjectId(session_id)}).deleted_count
        if cnt == 0:
            return {'error': 'Invalid session ObjectId'}
        return {'payload': {
            'session': session_id,
            'deleted': True
        }}

    @route('/<session_id>/start', methods=['PUT'])
    def start(self, session_id):
        if not ObjectId.is_valid(session_id):
            return {'error': 'Invalid session ObjectId'}
        session = flask_pymongo.db.sessions.find_one({'_id': ObjectId(session_id)})
        if not session:
            return {'error': 'Invalid session ObjectId'}
        session['start_time'] = datetime.datetime.utcnow()
        flask_pymongo.db.closed_sessions.insert_one(session)
        return {'payload': {
            'session': session_id,
            'deleted': True
        }}
