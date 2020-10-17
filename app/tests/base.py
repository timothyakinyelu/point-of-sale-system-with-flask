from flask_testing import TestCase
from app.db import db
from app import create_app
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