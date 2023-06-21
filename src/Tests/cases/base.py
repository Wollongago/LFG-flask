import datetime
import json
import logging
import os
import pprint
import sys
import unittest
from unittest import TestCase

from app import Application
from Extensions import flask_pymongo

__author__ = 'lonnstyle'
app = None

class BaseTest(TestCase):
    app_logs = True
    view_logs = True

    def create_app(self):
        print()
        print()
        print()
        print('{:+^70}'.format(' %s ' % self._testMethodName))
        global app
        if not app:
            app = Application(launch_mode='unit_test')()
        if not self.app_logs:
            logger = logging.getLogger(self.app.config['LOGGER_NAME'])
            logger.disabled = True
            logger.setLevel(logging.CRITICAL)
        if not self.view_logs:
            for logger_name in self.app.config['LOGGING']['loggers']:
                logger = logging.getLogger(logger_name)
                logger.disabled = True
                logger.setLevel(logging.CRITICAL)
        return app
    
    def setUp(self):
        self.client.__enter__()
        flask_pymongo.db.set_profiling_level(2)
        print()

    def tearDown(self):
        self.client.__exit__(None, None, None)
        flask_pymongo.db.set_profiling_level(0)
        flask_pymongo.db.system.profile.drop()

        flask_pymongo.db.user.drop()
        flask_pymongo.db.steam.drop()

        print('=> Results:')
        
    def show_operations(self):
        '''
        show_operations Print operations with DB from system.profile
        '''
        print('{:=^60}'.format(' DB Operations Profiler '))
        operations = list(flask_pymongo.db['system.profile'].find())
        print()
        print('Total operations: %s' % len(operations))
        print()
        for i in operations:
            if 'query' in i:
                pprint.pprint('{:=^40}'.format(' <{collection}:{operation}[{millis}ms]> '.format(
                    **{'operation':i['op'],
                       'collection':i['ns'],
                       'millis':i['millis']}
                )))
                pprint.pprint('Query:')
                pprint.pprint(i['query'])
                if i['op'] == 'update':
                    pprint.pprint('Update:')
                    pprint.pprint(i['updateobj'])
                print()