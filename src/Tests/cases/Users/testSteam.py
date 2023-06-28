import unittest

from Celery.tasks.steam import SteamParser
from Tests.cases.base import BaseTest


class TestSteam(BaseTest):
  
  def test_steam_sync(self):
    parser = SteamParser()
    get_steam_id = str(76561198034973737) # Testing case

    parser.update_parser(get_steam_id)
    parse_user_details = parser.get_user_details()
    parse_user_games = parser.get_user_games()
    parse_user_app_achievements = parser.get_user_app_achievements()

    testDocument = {
       "game_id": get_steam_id,
       "username": parse_user_details[0],
       "profile_url": parse_user_details[1],
       "country": parse_user_details[2],
       "games_owned": parse_user_games,
       "apex_achievements": parse_user_app_achievements
    }

    self.assertEqual(testDocument["game_id"], get_steam_id)
    self.assertEqual(testDocument["username"], parse_user_details[0])
    self.assertEqual(testDocument["profile_url"], parse_user_details[1])
    self.assertEqual(testDocument["country"], parse_user_details[2])
    self.assertEqual(testDocument["games_owned"], parse_user_games)
    self.assertEqual(testDocument["apex_achievements"], parse_user_app_achievements)
