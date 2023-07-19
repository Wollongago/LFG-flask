from bson import ObjectId
from Extensions import flask_pymongo
from marshmallow import Schema, ValidationError, fields, post_load, validates


class Session(Schema):
    roomTitle = fields.Str(required=True)
    selectedGame = fields.Int(required=True)
    selectedGameMode = fields.Str()
    partyCapacity = fields.Int(required=True)
    recommendedLevel = fields.Int(missing=0)
    owner = fields.Str(required=True)
    
    @validates('selectedGame')
    def validate_selectedGame(self, value):
        if not ObjectId.is_valid(value):
            raise ValidationError('Invalid selectedGame ObjectId')
        game = flask_pymongo.db.games.find_one({'_id': ObjectId(value)})
        if not game:
            raise ValidationError('Invalid selectedGame ObjectId')
        
    @validates('owner')
    def validate_owner(self, value):
        if not ObjectId.is_valid(value):
            raise ValidationError('Invalid owner ObjectId')
        user = flask_pymongo.db.users.find_one({'_id': ObjectId(value)})
        if not user:
            raise ValidationError('Invalid owner ObjectId')
        
    @post_load
    def make_session(self, data):
        data['user'] = ObjectId(data['owner'])
        session = flask_pymongo.db.sessions.insert_one(data)
        game = flask_pymongo.db.games.find_one({'_id': ObjectId(data['selectedGame'])})
        data['selectedGame'] = {
            'name' : game['name'],
            'appId': game['steam_appid']
        }
        return data
    
class SessionDump():
    def dump(self,data):
        data['id'] = str(data['_id'])
        del data['_id']
        return data
    
    def dump_many(self,data):
        return [self.dump(item) for item in data]