from Extensions.Nestable import NestableBlueprint

__author__ = 'KycKyc'

collection = NestableBlueprint('Session', __name__, url_prefix='/session')
collection.register_collection(__file__)