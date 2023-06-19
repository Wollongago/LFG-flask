from unittest import TestCase


class BaseTest(TestCase):
    def setUp(self):
        # get the database and switch to test database
        # set to 2 for profiling
        pass

    def tearDown(self):
        # set to 0 for profiling
        # drop all tables
        # drop system profile collection
        pass

    def show_operations(self):
        # print all operations from system profile collection
        # use pprint to print the operations
        pass
    