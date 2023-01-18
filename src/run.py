import os

from app import Application

__author__ = 'lonnstyle'

if __name__ == '__main__':
    application = Application(launch_mode='web_dev')()
    application.run(port=8000,host='0.0.0.0')
    