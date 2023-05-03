from Extensions.Nestable import NestableBlueprint

__author__ = 'KycKyc'

collection = NestableBlueprint('User', __name__, url_prefix='/user')
collection.register_collection(__file__)