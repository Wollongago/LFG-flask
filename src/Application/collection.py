from Extensions.Nestable import NestableBlueprint

__author__ = 'KycKyc'
collection = NestableBlueprint("Application", __name__)
collection.register_collection(__file__)