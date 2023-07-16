from Extensions.Nestable import NestableBlueprint

__author__ = 'lonnstyle'

collection = NestableBlueprint('Sessions', __name__, url_prefix='/sessions')
collection.register_collection(__file__)