# from Extensions.Parsers.steam_parse import SteamParser
# from Extensions import celery_app
from Extensions import flask_pymongo

# Testing purposes, since can't import SteamParser (import issues)
user_name = "test"
steam_id = "76561197960520747"


# @celery_app.task
def sync_user_profile():
#     # TODO: Add code to sync the user's profile to your application's database
#     parser = SteamParser()
    queryall = flask_pymongo.db.test.find()
    for user in queryall:
        if(flask_pymongo.db.test.find({"$or": [{"game_id": { "$exists": "false" }}, { "game_id": "null" }]})):
            flask_pymongo.db.test.update({"username": user_name}, {"$set": {"game_id": steam_id}})  
    return('Data sync success!')