from Extensions.Parsers.steam_parse import SteamParser
from Extensions import celery_app, flask_pymongo

@celery_app.task(name="steam.sync")
def sync_user_profile():
    print("sync_user_profile")
    # TODO: Add code to sync the user's profile to your application's database
    parser = SteamParser()
    
    users = flask_pymongo.db.user.find()
    for user in users:

        # Get user's STEAM ID then update that instance
        get_steam_id = user['steam_profile']['steam_id']
        
        # Create/Update User Instance
        parser.update_parser(get_steam_id)
        parse_user_details = parser.get_user_details()
        parse_user_games = parser.get_user_games()
        parse_user_app_achievements = parser.get_user_app_achievements()

        flask_pymongo.db.user.update_one(
                {"game_id": str(get_steam_id)},
                {
                    "$set": {
                        "username": parse_user_details[0],
                        "profile_url": parse_user_details[1],
                        "country": parse_user_details[2],
                        "games_owned": parse_user_games,
                        "apex_achievements": parse_user_app_achievements
                    }
                }
            )