from Extensions import flask_pymongo
from marshmallow import Schema, ValidationError, fields, post_load, pre_load, validate, validates, validates_schema
from bson import ObjectId

class User:
    fields = [
        '_id',
        'username',
        'password',
        'game_account',
        'avatar',
    ]

    def dump(self,data):
        # skip the fields if they are None
        return {k: v for k, v in data.items() if k in self.fields and v is not None}
    
    def dump_many(self,data_list):
        return [self.dump(data) for data in data_list]
class UserSchema(Schema):
    _id = fields.Str(dump_only=True)
    username = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    password = fields.Str(required=True, validate=validate.Length(min=8, max=50))
    email = fields.Email(required=True)
    game_account = fields.Str(validate=validate.Length(max=50))
    avatar = fields.Str(validate=validate.Length(max=100))

    @validates('user')
    def validate_user(self, value):
        if not flask_pymongo.db.users.find_one({'_id': ObjectId(value)}):
            raise ValidationError('User does not exist', 'user')
    
    # check if valid username
    @validates_schema
    def validate_username(self, data):
        if flask_pymongo.db.users.find_one({'username': data['username']}):
            raise ValidationError('Username already exists', 'username')
        
    # check if valid email
    @validates_schema
    def validate_email(self, data):
        if not flask_pymongo.db.users.find_one({'email': data['email']}):
            raise ValidationError('Email does not exist', 'email')
    
    
    @post_load
    def post_load(self, data):
        return User().dump(data)

