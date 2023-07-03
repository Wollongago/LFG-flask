import unittest

from Extensions import flask_pymongo
from Extensions.Parsers.steam_parse import SteamParser
from Tests.cases.base import BaseTest


class TestSteam(BaseTest):
  
  def test_steam_sync(self):
    parser = SteamParser()
    # test steam id
    flask_pymongo.db.user.insert_one({
      'steam_profile': {
        'steam_id': str(76561198034973737)
      }
    })

    for user in flask_pymongo.db.user.find():
      get_steam_id = user['steam_profile']['steam_id']
      parser.update_parser(get_steam_id)
      username, profile_url, country = parser.get_user_details()
      games = parser.get_user_games()
      app_achievements = parser.get_user_app_achievements()


    assert username == 'bayot'
    assert profile_url == 'https://steamcommunity.com/id/fourier69/'
    assert type(games) == list
    assert type(app_achievements) == list
    print(f'username: {username}, profile_url: {profile_url}, country: {country}, games: {games}, app_achievements: {app_achievements}')
