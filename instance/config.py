import os
from os.path import join, dirname

class Config(object):
   """Parent configuration class."""
   DEBUG = True
   CSRF_ENABLED = True
   SECRET = os.getenv('SECRET')


class DevelopmentConfig(Config):
   """Configurations for Development."""
   DEBUG = True
   use_reloader = True
   ADMIN_EMAIL = os.getenv('ADMIN_EMAIL')
   ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')


class TestingConfig(Config):
   """Configurations for Testing, with a separate test database."""
   TESTING = True
   DEBUG = True
   ADMIN_EMAIL = 'christinet@gmail.com',
   ADMIN_PASSWORD = 'asdfdsaf'


class StagingConfig(Config):
   """Configurations for Staging."""
   DEBUG = True


class ProductionConfig(Config):
   """Configurations for Production."""
   DEBUG = False
   TESTING = False


app_config = {
   'development': DevelopmentConfig,
   'testing': TestingConfig,
   'staging': StagingConfig,
   'production': ProductionConfig,
}