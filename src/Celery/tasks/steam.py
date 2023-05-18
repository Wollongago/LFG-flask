from Extensions.Parsers.steam_parse import SteamParser
from Application.Api.latest.__schemas import user
#import requests
from Extensions import flask_pymongo
from Extensions import celery_app

@celery_app.task
def update_user_schema():
    profile = get_user_details()
    user.fields.game_account = profile('steamid')

@celery_app.task
def sync_user_profile(steam_id):
    with celery_app.app_context():
        # TODO: Add code to sync the user's profile to your application's database
        for users in flask_pymongo.db.users.find():
            flask_pymongo.save_file(users)
        





