from steam import Steam

from src.credentials import STEAM_API_KEY

#import os

steam = Steam(STEAM_API_KEY)

class SteamParser():
    def get_user_details():
        user = steam.users.get_user_details("<steam_id>")

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
    #print(os.getcwd)
    user = get_user_details("76561197960520747")
    print(user)
