
from Extensions.Nestable import NestableBlueprint

__author__ = 'KycKyc'

collection = NestableBlueprint('Api', __name__,url_prefix="/api")
collection.register_collection(__file__)
