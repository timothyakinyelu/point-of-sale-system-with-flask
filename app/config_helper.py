from app.config import *

def load_config(MODE):
    """ Checks which environment variables to load app with."""
    
    try:
        if MODE == 'production':
            return ProductionConfig
        else:
            return DevelopmentConfig
    except EnvironmentError:
        raise EnvironmentError('Invalid environment for app state.')
    