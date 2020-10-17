from app.config import *

def load_config(MODE):
    """ Checks which environment variables to load app with."""
    
    try:
        if MODE == 'production':
            return ProductionConfig
        elif MODE == 'testing':
            return TestConfig
        else:
            return DevelopmentConfig
    except ImportError:
        return BaseConfig
    