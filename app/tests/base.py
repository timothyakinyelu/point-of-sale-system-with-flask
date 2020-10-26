from flask_testing import TestCase
from app.db import db
from app import create_app
from app.models.user import User
from app.models.permission import Permission
from app.models.role import Role
from app.forms import *
from app.config_helper import load_config

app = create_app()

class BaseCase(TestCase):
    """ Parent class for Test Cases. """
    
    def create_app(self):
        mode = 'testing'
        Config = load_config(mode)
        app.config.from_object(Config)
        return app
    
    def setUp(self):
        db.create_all()
        
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        
    def createUser(self):
        user = User(username = 'Juniper', password = 'password')
        user.set_password('password')
        db.session.add(user)
        db.session.commit()
        
        return user
    
    def loginUser(self):
        login = LoginForm(username = 'Juniper',
            password = 'password'
        )
        
        return login
    
    def createUserRole(self):
        role = Role(title = 'Cashier')
        db.session.add(role)
        db.session.commit()
        
        return role

    def createUserPermission(self):
        permission = Permission(name = 'Create User')
        db.session.add(permission)
        db.session.commit()
        
        return permission