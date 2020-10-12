from app.config import *

def load_config(MODE):
    try:
        if MODE == 'production':
            return ProductionConfig
        else:
            return DevelopmentConfig
    except EnvironmentError:
        raise EnvironmentError('Invalid environment for app state.')