from steam import Steam
#from src.credentials import STEAM_API_KEY

steam = Steam('STEAM_API_KEY')

class SteamParser():
    def get_user_details(steam_id):
        user = steam.users.get_user_details(steam_id)
        steamid_value = user.get("player", "not found").get("steamid", "not found")
        username_value = user.get("player", "not found").get("personaname", "not found")
        print (steamid_value, username_value)
        return (steamid_value, username_value)

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
# if __name__ == "__main__":
#     user = SteamParser.get_user_details("76561197960520747")

