
from Extensions.MongoDB.json import json_encode
from Extensions.Nestable import NestableBlueprint
from flask import Response

__author__ = 'KycKyc'

collection = NestableBlueprint('Api', __name__,url_prefix="/api")
collection.register_collection(__file__)

@collection.after_request
def encode_response(response):
    if isinstance(response, dict):
        return Response(response=json_encode.encode(response),
                        mimetype="application/json")
    else:
        return response