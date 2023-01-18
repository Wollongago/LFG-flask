import logging
import logging.config
import os

from flask import Flask

__author__ = 'lonnstyle'

class Application:
    """
    Application Fabricator.
    """

    def __init__(self,launch_mode):
        """Initiate the Flask app

        Args:
            launch_mode: which mode is the app being launched
        """
        self.app = Flask(__name__)
        self.launch_mode = launch_mode
        modes = {'web_dev':('config.Development',self.make_http)}

        if launch_mode not in modes:
            raise KeyError('WRONG LAUNCH MODE')
        self.config = modes[launch_mode][0]
        self.make_app = modes[launch_mode][1]
    
    def __call__(self):
        """
        
        Returns:
        """
        # Load Flask config
        self.app.config.from_object(self.config)
        # Setup the Logs
        self.app.logger_name = self.app.config['LOGGER_NAME']
        self.app._logger = logging.getLogger(self.app.logger_name)
        # logging.config.dictConfig(self.app.config['LOGGING'])
        return self.make_app()

    def make_http(self):
        """Make WSGI Application
        
        Returns:
            Flask application   
        """
        return self.app