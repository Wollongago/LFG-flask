import json
from copy import deepcopy

from credentials import STEAM_API_KEY
from steam import Steam

steam = Steam(STEAM_API_KEY)

class SteamParser():
    def update_parser(self, steam_id):
        if type(steam_id) == int:
            steam_id = str(steam_id)
        self.steam_id = steam_id

    # Gets any user's profile data/details
    def get_user_details(self):
        self.user = steam.users.get_user_details(self.steam_id)
        self.username_value = self.user.get("player", None).get("personaname", None)
        self.profile_url = self.user.get("player", None).get("profileurl", None)
        self.country_loc = self.user.get("player", None).get("loccountrycode", None)
        # print (self.username_value, self.profile_url, self.country_loc)
        return (self.username_value, self.profile_url, self.country_loc)
    
    # Gets any user's whole game-library and their full playtime in minutes
    def get_user_games(self):
        self.user_games = steam.users.get_owned_games(self.steam_id)

        # Initializing list
        self.game_list = []

        # Initializing dictionary with keys and NO values
        self.game_dict = {}
        keys = ["game_name", "total_playtime", "2weeks_playtime"]
        for key in keys:
            self.game_dict[key] = None

        # Filtering out only needed data
        for game in self.user_games.get("games", None):
            self.game_dict["game_name"] = game.get("name")
            self.game_dict["total_playtime"] = game.get("playtime_forever")
            self.game_dict["2weeks_playtime"] = game.get("playtime_2weeks")
            self.game_list.append(deepcopy(self.game_dict))
        # print(self.game_list)
        return(self.game_list)
    
    # Gets any user's app achievements (in this case, Apex Legends)
    def get_user_app_achievements(self):
        self.user_app_details = steam.apps.get_user_achievements(self.steam_id, 1172470) # 1172470 = APEX LEGENDS ID ON STEAM
        self.achievements = self.user_app_details.get("playerstats", None).get("achievements", None)
        return self.achievements
    
    def get_game_detail(self, game_id):
        self.game_detail = steam.apps.get_app_details(game_id)
        # I have no idea why it return a string instead of a dict, just load it as json
        self.game_detail = json.loads(self.game_detail)
        return self.game_detail