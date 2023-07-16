from bson import ObjectId
from Extensions import flask_pymongo
from marshmallow import Schema, ValidationError, fields, post_load, pre_load, validate, validates, validates_schema


class User:
    fields = [
        '_id',
        'steam_profile'
    ]

    def dump(self,data):
        # skip the fields if they are None
        return {k: v for k, v in data.items() if k in self.fields and v is not None}
    
    def dump_many(self,data_list):
        return [self.dump(data) for data in data_list]
class UserSchema(Schema):
    _id = fields.Str(dump_only=True)
    steam_profile = fields.Dict()

    @validates('user')
    def validate_user(self, value):
        if not flask_pymongo.db.users.find_one({'_id': ObjectId(value)}):
            raise ValidationError('User does not exist', 'user')
    
    
    @post_load
    def post_load(self, data):
        return User().dump(data)

