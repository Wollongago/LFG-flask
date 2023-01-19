import logging

from Extensions.Nestable.Classy import Classy42

logger = logging.getLogger('Api')

class TestView(Classy42):
    decorators = []

    def index(self):
        return 'test v1'