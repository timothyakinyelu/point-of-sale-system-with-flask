from app.db import db
from .pivots import permission_user_table
from flask_login import UserMixin

class Users(db.Model, UserMixin):
    __tablename__ = 'users'
    
    id = db.Column(
        db.Integer,
        primary_key = True,
        autoincrement = True
    )
    username = db.Column(
        db.String(100),
        nullable = False
    )
    password = db.Column(
        db.String(100),
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
        'Permissions', 
        secondary = permission_user_table, 
        backref = 'user', 
        lazy = 'joined'
    )
    
    def __init__(self, name):
        self.active = False