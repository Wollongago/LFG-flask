import logging
import re

import requests
from Extensions import flask_pymongo
from Extensions.Nestable.Classy import Classy42
from Extensions.Parsers.steam import SteamParser
from flask import Response, current_app, request, url_for
from werkzeug.exceptions import BadRequest, InternalServerError
