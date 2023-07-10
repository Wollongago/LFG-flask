import logging
import re

import requests
from Application.models import User
from Extensions import flask_pymongo
from Extensions.Auth.actions import login
from Extensions.Nestable.Classy import Classy42
from Extensions.Parsers.steam import SteamParser
from flask import Response, current_app, request, url_for
from werkzeug.exceptions import BadRequest, InternalServerError

logger = logging.getLogger('Frontend')

class SteamView(Classy42):
    decorators = []
    trailing_slash = False

    def index(self):
        # FIXME: change the url to production url
        # this is 8000 as this is API port
        host_url = 'http://localhost:8000'
        return_to = host_url + '/auth/steam/accept'

        additional_params = []

        _next = request.args.get('next')
        if _next:
            additional_params.append(('next', _next))

        _auth_type = request.args.get('auth_type')
        if _auth_type and _auth_type in ['cookie', 'app', 'header']:
            additional_params.append(('auth_type', _auth_type))

        _device_id = request.args.get('device_id')
        if _device_id and len(_device_id) <= 64:
            additional_params.append(('device_id', _device_id))

        if len(additional_params) > 0:
            return_to += '?' + '&'.join(['{}={}'.format(k, v) for k, v in additional_params])

        params = {'openid.ns': 'http://specs.openid.net/auth/2.0',
                  'openid.mode': 'checkid_setup',
                  'openid.return_to': return_to,
                  'openid.realm': return_to,
                  'openid.ns.sreg': 'http://openid.net/extensions/sreg/1.1',
                  'openid.claimed_id': 'http://specs.openid.net/auth/2.0/identifier_select',
                  'openid.identity': 'http://specs.openid.net/auth/2.0/identifier_select'}
        req = requests.Request('GET',
                               url='https://steamcommunity.com/openid/login',
                               params=params)
        return Response(status=302, headers={'Location': str(req.prepare().url)})
    
    def link(self):
        '''
        link link steam account to current user
        '''
        # skip it as we don't have user system yet, directly login with steam
        return Response(status=302, headers={'Location': url_for('SteamView:accept')})
    
    def accept(self):
        '''
        accept steam login, store steam-profile into and tokens into database
        :return:
        '''

        # it should always be False, since we don't have user system yet
        linkage = request.args.get('link') is not None
        logger.debug('linkage: {}'.format(linkage))

        # get `next` query parameter
        _next = request.args.get('next')
        logger.debug('next: {}'.format(_next))

        # get `auth_type` query parameter
        _auth_type = request.args.get('auth_type', 'cookie')
        logger.debug('auth_type: {}'.format(_auth_type))
        
        # get `device_id` query parameter
        _device_id = request.args.get('device_id')
        logger.debug('device_id: {}'.format(_device_id))

        # prepare validation request
        data_from_steam = {}
        for arg in request.args:
            data_from_steam[arg] = request.args[arg]
        logger.debug('Steam response: {}'.format(data_from_steam))
        data_from_steam['openid.mode'] = 'check_authentication'

        logger.debug('Additional validation request to Steam')
        req = requests.post('https://steamcommunity.com/openid/login', data=data_from_steam)
        if req.status_code != 200:
            logger.warning(f'Steam service unavailable? (code - {req.status_code})')
            raise InternalServerError(f'Steam validation request failed, code - {req.status_code}')
        
        # Check if user is valid
        if not re.compile('true').search(req.text):
            if re.compile('false').search(req.text):
                logger.warning('Steam validation failed, user is not valid')
                raise BadRequest('Steam validation failed, user is not valid')
            logger.error(f'Unknown Steam validation response - {req.text}')
            raise InternalServerError(f'Unknown Steam validation response')
        
        # User validation passed
        regexp_steamid = re.compile('(?<=/openid/id/).*$')
        steam_user_id = regexp_steamid.search(data_from_steam['openid.claimed_id']).group(0)
        logger.debug('Steam user id: {}'.format(steam_user_id))

        # get user profile
        parser = SteamParser()
        parser.update_parser(steam_user_id)
        steam_profile = {}
        username, profile_url, loc = parser.get_user_details()
        steam_profile['username'] = username
        steam_profile['profile_url'] = profile_url
        steam_profile['loc'] = loc
        steam_profile['games'] = parser.get_user_games()

        # link steam account to current user
        if linkage:
            # we don't have user system yet, so skip it
            pass
            return Response(status=302, headers={'Location': 'http://localhost:3000'})
        
        # login with steam
        logger.debug('Login with steam')
        user = flask_pymongo.db.users.find_one({'steam_profile.steam_id': steam_user_id})
        redirect_location = 'http://localhost:3000'
        if user is None:
            logger.debug('User not found, creating new user')
            steam_profile['steam_id'] = steam_user_id
            user = User.create_from({'steam_profile': steam_profile})
            logger.debug('New user created')
            logger.debug(f'User: {user}')
            user.insert()
        else:
            user = User(_data=user)
            if _next:
                redirect_location = _next
        
        login(user,auth_type=_auth_type)

        return Response(status=302,headers={'Location': redirect_location})