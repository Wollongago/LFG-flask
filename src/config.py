import os

__author__ = 'lonnstyle'

try:
    import credentials
except ImportError:
    raise RuntimeError("Attempt to run Flask without `credentials.py` file.")

class Global(object):
    DEBUG = False
    TESTING = False
    SHOW_ENDPOINTS = False
    APP_NAME = 'LFG'

    LOGGER_NAME = APP_NAME
    BASE_DIR = os.path.realpath(__file__).rsplit('/',2)[0]
    PRINT_VERBOSE_ROUTES = False
    MAX_CONTENT_LENGTH = 16*1024*1024

    # Sign cookies and other things.
    SECRET_KEY = credentials.SECRET_KEY

    # MONGOENGINE SETTINGS
    MONGODB_SETTINGS = {"DB":"LFG",
                        "USERNAME":"",
                        "PASSWORD":"",
                        "HOST":'mongodb',
                        "PORT":27017}
    
    # PY-MONGO SETTINGS
    MONGO_URI = "mongodb://mongodb:27017/LFG?maxPoolSize=200"

    # TODO:AMPQ Broker SETTINGS

    # TODO:Cache

class Development(Global):
    DEBUG = True
    SHOW_ENDPOINTS = True
    EXPLAIN_TEMPLATE_LOADING = False

    SERVER_NAME = 'lookingfor.group'
    PREFFERED_URL_SCHEME = 'http'
    SESSION_COOKIE_SECURE = False

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': "[%(asctime)s] %(levelname)s [%(name)s:%(pathname)s:%(lineno)s] %(message)s",
                'datefmt': "%Y-%m-%d %H:%M:%S"
            },
            'simple': {
                'format': '[%(levelname)s] %(message)s'
            },
        },
        'filters': {
            'test_filter': {
                '()': 'Extensions.Logs.filters.TestFilter',
            }
        },
        'handlers': {
            'null': {
                'level': 'DEBUG',
                'class': 'logging.NullHandler',
            },
            'simple_console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'simple'
            },
            'verbose_console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'verbose'
            },
            'buffering_error': {
                'level': 'DEBUG',
                'class': 'Extensions.Logs.handlers.BufferingErrorHandler',
                'capacity': 50,
                'formatter': 'verbose'
            }
        },
        'loggers': {
            Global.LOGGER_NAME: {
                'handlers': ['verbose_console'],
                'level': 'DEBUG',
            },
            'Api': {
                'handlers': ['verbose_console'],
                'level': 'DEBUG',
            },
            'Frontend': {
                'handlers': ['verbose_console'],
                'level': 'DEBUG',
            },
            'authlib': {
                'handlers': ['verbose_console'],
                'level': 'DEBUG',
            }

        }
    }