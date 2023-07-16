from Extensions.Nestable import NestableBlueprint

__author__ = 'lonnstyle'

collection = NestableBlueprint('Game', __name__, url_prefix='/game')
collection.register_collection(__file__)