from Extensions.Nestable import NestableBlueprint

collection = NestableBlueprint('Frontend.auth', __name__,url_prefix="/auth")
collection.register_collection(__file__)