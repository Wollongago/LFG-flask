import logging
import os
import string

import requests
from bson import ObjectId
from Extensions import flask_pymongo
from Extensions.Parsers.steam import SteamParser
from flask_script import Manager

logger = logging.getLogger('Manager')

__author__ = 'lonnstyle'

steam_manager = Manager(usage='Perform Steam related tasks')

@steam_manager.command
def update_games():
    '''
    update_games will update the game collection with the latest games from steam
    '''
    logger.info('Updating Games')
    games = flask_pymongo.db.games
    parser = SteamParser()
    fields = ['type','name','steam_appid','controller_support','detailed_description','about_the_game','short_description','supported_languages','header_image','website','developers','publishers','platforms','categories','genres','background','background_raw']
    for game in games.find():
        # idk why it is a float, but just cast it to int
        game_id = int(game['steam_appid'])
        game_info = parser.get_game_detail(game_id)

        if game_info:
            # serialize game_info
            # on theory, the outest most key is the game_id, but we just use the first key
            game_info = game_info[list(game_info.keys())[0]]
            logger.info(f'Updating Game: {game_info["data"].get("name","")}<id:{game_id}>')
            if game_info['success'] == False:
                logger.error('Game not found: %s', game_id)
                continue
            game_info = game_info['data']
            to_delete = list(set(game_info.keys()) - set(fields))
            for key in to_delete:
                del game_info[key]
            game_name = game_info['name'].lower().replace(' ','_')
            game_name = ''.join(filter(set(string.ascii_letters + '_').__contains__, game_name))
            for key in ['header_image','background','background_raw']:
                # save image to file and update path

                # strip url to get file name
                file_name = game_info[key].split('/')[-1]
                file_name = file_name.split('?')[0]
                out_path = f'static/assets/games/{game_name}_{file_name}'
                os.makedirs(os.path.dirname(out_path), exist_ok=True)

                print(f'Download remote asset from: {game_info[key]} to: {out_path}')
                r = requests.get(game_info[key], stream=True)
                if r.status_code == 200:
                    with open(out_path, 'wb') as f:
                        for chunk in r:
                            f.write(chunk)
                    game_info[key] = out_path
            # hardcode the library portait image as not shown in steam api
            file_name = 'library_portrait.jpg'
            out_path = f'static/assets/games/{game_name}_{file_name}'
            os.makedirs(os.path.dirname(out_path), exist_ok=True)
            print(f'Download remote asset from: https://cdn.akamai.steamstatic.com/steam/apps/{game_id}/library_600x900.jpg to: {out_path}')
            r = requests.get(f'https://cdn.akamai.steamstatic.com/steam/apps/{game_id}/library_600x900.jpg', stream=True)
            if r.status_code == 200:
                with open(out_path, 'wb') as f:
                    for chunk in r:
                        f.write(chunk)
                game_info['library_portrait'] = out_path

            flask_pymongo.db.games.update({'_id': game['_id']}, {'$set': game_info}, upsert=False)
        else:
            logger.error('Game not found: %s', game_id)