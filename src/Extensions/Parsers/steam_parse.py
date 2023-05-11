from steam import Steam
import os
#from src.credentials import STEAM_API_KEY
steam = Steam(STEAM_API_KEY)

class SteamParser():
    def get_game_details():
        apex_app_id = 1172470

        # arguments: app_id
        user = steam.apps.get_game_details(apex_app_id)

    def get_user_game_details():
        # arguments: steam_id, app_id
        user = steam.apps.get_user_game_details("<steam_id>", "<app_id>")

    def get_user_game_achievements():
        # arguments: steam_id, app_id
        user = steam.apps.get_user_game_achievements("<steam_id>", "<app_id>")

# testing output
if __name__ == "__main__":
    print(os.getcwd)
    user = steam.users.get_user_details("76561197960520747")
    print(user)
