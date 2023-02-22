import logging
import logging.config
import os

from Extensions.Nestable.Flask import Flask42
from Extensions.Nestable.utils import import_string

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
        self.app = Flask42(__name__)
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
        blue_site = import_string("Application.collection:collection")
        self.app.register_blueprint(blue_site)
        if self.app.config['DEBUG'] and self.app.config['SHOW_ENDPOINTS']:
            print()
            print()
            print('Application Endpoints')
            print()
            collections = {}
            for _endpoint in self.app.url_map._rules_by_endpoint:
                _collection = _endpoint.rsplit('.', 1)[0]
                if _collection not in collections:
                    collections[_collection] = []
                for _rule in self.app.url_map._rules_by_endpoint[_endpoint]:
                    tmp = []
                    for is_dynamic, data in _rule._trace:
                        if is_dynamic:
                            tmp.append(u'<%s>' % data)
                        else:
                            tmp.append(data)
                    readable_path = repr((u''.join(tmp)).lstrip(u'|')).lstrip(u'u')
                    collections[_collection].append({'endpoint': _endpoint, 'url': readable_path})
        for _collection in collections:
            print()
            print(_collection)
            for view in collections[_collection]:
                print(' - {:⋅<60}▸ {:<60}'.format(view['url'].strip('\''), view['endpoint']))
        print()
        return self.app