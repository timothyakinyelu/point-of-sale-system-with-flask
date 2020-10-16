import os
from flask import Flask, flash, redirect, url_for
from app.config_helper import load_config
from flask_login import LoginManager

login_manager = LoginManager()

def create_app():
    app = Flask(__name__, template_folder='./templates')
    mode = app.env
    
    Config = load_config(mode)
    app.config.from_object(Config)
    
    from .db import db
    db.init_app(app)
    login_manager.login_view = 'nonAuth.login'
    login_manager.init_app(app)
    
    from app.models import employee, permission, role, user, pivots
    @login_manager.user_loader
    def load_user(user_id):
        """Check if user is logged-in on every page load."""
        
        if user_id is not None:
            return user.User.query.get(user_id)
        return None
    
    @login_manager.unauthorized_handler
    def unauthorized():
        """Redirect unauthorized users to Login page."""
        
        flash('You must be logged in to view that page.')
        return redirect(url_for('nonAuth.login'))
    
    with app.app_context():
        # add route blueprints here
        from app.routes.auth import access_routes
        from app.routes.non_auth import nonAccess_routes
        
        app.register_blueprint(access_routes.auth)
        app.register_blueprint(nonAccess_routes.nonAuth)
        
        db.create_all()
        
        return app