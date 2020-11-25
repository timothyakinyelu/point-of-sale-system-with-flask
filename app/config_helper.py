from app.config import *
from functools import wraps
from flask_login import current_user
from flask import flash, redirect, url_for, request

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
    
    
def required_permissions(*perms):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if current_user.hasPermissionTo(perms):
                return f(*args, **kwargs)
            return redirect(url_for('nonAuth.unauthorized'))
        return wrapped
    return wrapper
            