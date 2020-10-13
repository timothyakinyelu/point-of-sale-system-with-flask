import os
from flask import Flask
from app.config_helper import load_config

def create_app():
    app = Flask(__name__, template_folder='./templates')
    mode = app.env
    
    Config = load_config(mode)
    app.config.from_object(Config)
    
    from .db import db
    db.init_app(app)
    
    from app.models import employee, permission, role, user, pivots
    
    with app.app_context():
        # add route blueprints here
        from app.routes.auth import home
        from app.routes.non_auth import users
        app.register_blueprint(home.auth)
        app.register_blueprint(users.nonAuth)
        
        db.create_all()
        
        return app