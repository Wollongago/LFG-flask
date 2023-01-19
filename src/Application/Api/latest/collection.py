import os

from Extensions.Nestable import NestableBlueprint

__author__ = 'KycKyc'

collection = NestableBlueprint('v1', __name__, url_prefix='/v1')
collection.register_collection(__file__)
