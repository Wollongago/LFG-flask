from marshmallow import Schema, fields, validate

class UserSchema(Schema):
    username = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    password = fields.Str(required=True, validate=validate.Length(min=8, max=50))
    email = fields.Email(required=True)
    game_account = fields.Str(validate=validate.Length(max=50))
    avatar = fields.Str(validate=validate.Length(max=100))


