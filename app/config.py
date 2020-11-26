import os

class BaseConfig: 
    """ Parent configuration class."""
    
    SECRET_KEY = os.environ.get('SECRET_KEY')
    WTF_CSRF_ENABLED = True
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CURRENCY_ICON = '₦'
    JSON_SORT_KEYS = False
    
    
class DevelopmentConfig(BaseConfig):
    """ Config for development purposes. """
    
    DEBUG = os.environ.get('DEBUG')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    TEMPLATES_AUTO_RELOAD = True
    
class ProductionConfig(BaseConfig):
    """ Config for production ready app."""
    
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    
class TestConfig(BaseConfig):
    """ Config for testing purposes only."""
     
    DEBUG = True
    WTF_CSRF_ENABLED = False
    TESTING = True
    HASH_ROUNDS = 1
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URI')
    PRESERVE_CONTEXT_ON_EXCEPTION = False