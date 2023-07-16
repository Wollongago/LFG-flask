import logging

from bson import ObjectId
from Extensions import flask_pymongo
from Extensions.Nestable.Classy import Classy42
from Extensions.Nestable.flask_classy import route

__author__ = 'lonnstyle'

logger = logging.getLogger('Api')

class GameView(Classy42):
    decorators = []
    trailing_slash = False
    route_base = '/'
    
    @route('/<game_id>')
    def index(self,game_id):
        '''
        index return a game object if it exists

        :param game_id: ObejctId
        :type game_id: str
        '''
        if not ObjectId.is_valid(game_id):
            return {'error': 'invalid game_id'}
        game = flask_pymongo.db.games.find_one({'_id': ObjectId(game_id)})
        if not game:
            return {'error': 'game not found'}
        del game['_id']
        return {'payload': game}