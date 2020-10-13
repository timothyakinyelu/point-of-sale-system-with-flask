from app.db import db
from .pivots import permission_user_table
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    
    id = db.Column(
        db.Integer,
        primary_key = True,
        autoincrement = True
    )
    username = db.Column(
        db.String(100),
        unique = True,
        nullable = False
    )
    password = db.Column(
        db.String(200),
        nullable = False
    )
    role_id = db.Column(
        db.Integer,
        db.ForeignKey('roles.id')
    )
    active = db.Column(
        db.Boolean
    )
    permissions = db.relationship(
        'Permission', 
        secondary = permission_user_table, 
        backref = 'users', 
        lazy = 'joined'
    )
    
    def __init__(self):
        self.active = False
        
    def set_password(self, password):
        self.password = generate_password_hash(password, method='sha256')
        
    def check_password(self, password):
        return check_password_hash(self.password, password)