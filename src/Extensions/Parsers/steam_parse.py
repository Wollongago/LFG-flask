from steam import Steam
#from src.credentials import STEAM_API_KEY

steam = Steam('STEAM_API_KEY')

class SteamParser():
    def __init__(self, steam_id):
        self.steam_id = steam_id
        print('Constructor called!')

    def get_user_details(self, steam_id):
        self.user = steam.users.get_user_details(steam_id)
        self.steamid_value = self.user.get("player", "not found").get("steamid", "not found")
        self.username_value = self.user.get("player", "not found").get("personaname", "not found")
        print (self.steamid_value, self.username_value)
        return (self.steamid_value, self.username_value)

# testing output
if __name__ == "__main__":
    parser = SteamParser("76561197960520747")
    user = parser.get_user_details("76561197960520747")

