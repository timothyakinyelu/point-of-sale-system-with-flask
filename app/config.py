import os

class BaseConfig: 
    SECRET_KEY = os.environ.get('SECRET_KEY')
    CSRF_ENABLED = True
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    
class DevelopmentConfig(BaseConfig):
    DEBUG = os.environ.get('DEBUG')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')
    
class ProductionConfig(BaseConfig):
    SECRET_KEY = 'some_random_aplhanumeric_string'
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'postgresql:///example'