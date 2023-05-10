from steam import Steam
from decouple import config


KEY = config("STEAM_API_KEY")
steam = Steam(KEY)

class SteamParser():
    def get_game_details():
        apex_app_id = 1172470
        steam = Steam(KEY)

        # arguments: app_id
        user = steam.apps.get_game_details(apex_app_id)

    def get_user_game_details():
        steam = Steam(KEY)

        # arguments: steam_id, app_id
        user = steam.apps.get_user_game_details("<steam_id>", "<app_id>")

    def get_user_game_achievements():
        steam = Steam(KEY)

        # arguments: steam_id, app_id
        user = steam.apps.get_user_game_achievements("<steam_id>", "<app_id>")

# testing output
user = steam.users.get_user_details("76561197960520747")
print(user)
