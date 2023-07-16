import logging

from marshmallow import Schema, fields

from Extensions import flask_pymongo

class Game(Schema):
    '''
    From Game collection
    '''

    name = fields.