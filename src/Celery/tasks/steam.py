from Extensions.Parsers.steam_parse import SteamParser
from Extensions import celery_app, flask_pymongo

@celery_app.task(name="steam.sync")
def sync_user_profile():
    print("sync_user_profile")
    # TODO: Add code to sync the user's profile to your application's database
    parser = SteamParser("76561197960520747")
    parser.get_user_details()
    parser.get_user_games()
    parser.get_user_app_achievements()

    queryall = flask_pymongo.db.test.find()
    for user in queryall:
        # if(flask_pymongo.db.test.find({"$or": [{"game_id": { "$exists": False }}, { "game_id": None} ]})):
        if(flask_pymongo.db.test.find({"username": "ronjosh"})): # For testing-case
            flask_pymongo.db.test.update_many({"username": parser.username_value}, 
                                              {"$set": {"game_id": parser.steamid_value,
                                                        "profile_url": parser.profile_url,
                                                        "country": parser.country_loc,
                                                        "games_owned": parser.game_list,
                                                        "apex_achievements": [parser.achievements]}})
    return('Data sync success!')