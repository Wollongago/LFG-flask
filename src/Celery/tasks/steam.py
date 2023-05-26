# from Extensions.Parsers.steam_parse import SteamParser
# from Application.Api.latest.user.views import *
import sys
# from Extensions import celery_app
from flask import Flask
from Extensions import flask_pymongo


# Testing purposes, since can't import SteamParser (import issues)
user_name = "ronjosh"
steam_id = "76561197960520747"
print (user_name, steam_id)


# @celery_app.task
# @app.route("/")
# def sync_user_profile(user_name, steam_id):
def sync_user_profile():
#     # TODO: Add code to sync the user's profile to your application's database
#     parser = SteamParser()
#     steam_id = "76561197960520747" #testing purpose
#     UserSteamId = parser.get_user_details(steam_id)
    # users = flask_pymongo.db.test.find({"$or": [{"game_id": { "$exists": "false" }}, { "game_id": "null" }]})
    flask_pymongo.db.test.insertOne({"username": "ronjosh", "game_id": "null"})
    users = flask_pymongo.db.test.find()
    return users
    # for user in users:
        # if(user.username == user_name): #not sure if this line is correct
        # # if(flask_pymongo.db.test.find_or_404({"username": "user_name"})):
        #     user.game_id = steam_id #UserSteamId('steamid') 
        #     flask_pymongo.db.test.updateOne({"username": user_name}, {"$set": {"game_id": steam_id}}) #variable could be wrong
        #     flask_pymongo.save_file()                                          
        # return 'Database synchronized successfully!' 
    
# sync_user_profile("ronjosh", "76561197960520747")
sync_user_profile()
modulename = 'flask_pymongo'
if modulename not in sys.modules:
    print ('You have not imported the {} module'.format(modulename))