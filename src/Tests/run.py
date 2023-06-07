import unittest
from app import Application
from Extensions import flask_pymongo

class BaseTest(unittest.TestCase):
    app = None
    def create_app(self):
    # Make app a global app
        global app
        # Create app with launch mode set to unit test
        if app is None:
            app = Application(launch_mode='unit test')
            return app  

    def setUp(self):
        # Set up any necessary test data
        self.client.__enter__()
        flask_pymongo.db.set_profiling_level(2)
        pass
        
    def tearDown(self):
        # Reset the database by dropping all tables, etc.
        self.client.__exit__(None,None,None)
        flask_pymongo.db.set_profiling_level(0)
        
