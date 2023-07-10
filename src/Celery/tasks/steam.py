from Extensions import celery_app, flask_pymongo
from Extensions.Parsers.steam import SteamParser


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
        username, profile_url, country = parser.get_user_details()
        games = parser.get_user_games()
        app_achievements = parser.get_user_app_achievements()

        flask_pymongo.db.user.update_one(
                {"game_id": str(get_steam_id)},
                {
                    "$set": {
                        "username": username,
                        "profile_url": profile_url,
                        "country": country,
                        "games_owned": games,
                        "apex_achievements": app_achievements
                    }
                }
            )