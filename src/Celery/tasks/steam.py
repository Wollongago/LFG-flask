from Extensions.Parsers.steam_parse import SteamParser
from Extensions import celery_app, flask_pymongo

@celery_app.task(name="steam.sync")
def sync_user_profile():
    print("sync_user_profile")
    # TODO: Add code to sync the user's profile to your application's database
    steam_ids = [76561197960520747, 76561198034973737]
    parser_instances = []

    for steam_id in steam_ids:
        parser = SteamParser()
        parser.create_parser(steam_id)
        parser_instances.append(parser)

    for parser in parser_instances:
        parser.get_user_details()
        parser.get_user_games()
        parser.get_user_app_achievements()
        print(parser)

        query = {"game_id": str(parser.steam_id)}
        queryall = flask_pymongo.db.user.find(query)

        for user in queryall:
            if user.get("game_id") == str(parser.steam_id):
                flask_pymongo.db.user.update_one(
                    {"game_id": str(parser.steam_id)},
                    {
                        "$set": {
                            "username": parser.username_value,
                            "profile_url": parser.profile_url,
                            "country": parser.country_loc,
                            "games_owned": parser.game_list,
                            "apex_achievements": parser.achievements
                        }
                    }
                )