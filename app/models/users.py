from app.db import db
from .pivots import permission_user_table, role_user_table

class Users(db.Model):
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
    active = db.Column(db.Boolean())
    permissions = db.relationship(
        'Permissions', 
        secondary = permission_user_table, 
        backref = 'user', 
        lazy = 'joined'
    )
    roles = db.relationship(
        'Roles', 
        secondary = role_user_table, 
        backref = 'user', 
        lazy = 'joined'
    )