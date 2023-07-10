from Extensions.Nestable import NestableBlueprint

collection = NestableBlueprint('Frontend', __name__,url_prefix="")

collection.register_collection(__file__)