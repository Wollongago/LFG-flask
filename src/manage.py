import logging.config

from app import Application  # assets
from Extensions.Managers.steam import steam_manager
from flask_script import Manager

__author__ = 'lonnstyle'

logger = logging.getLogger('Manager')

app = Application(launch_mode='manager')()
manager = Manager(app)
manager.add_command('steam', steam_manager)

if __name__ == '__main__':
    manager.run()