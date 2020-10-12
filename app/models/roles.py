from app.db import db
from .pivots import permission_role_table

class Roles(db.Model):
    __tablename__ = 'roles'
    
    id = db.Column(
        db.Integer,
        primary_key = True,
        autoincrement = True
    )
    title = db.Column(
        db.String(100),
        nullable = False
    )
    permissions = db.relationship(
        'Permissions', 
        secondary = permission_role_table, 
        backref = 'role', 
        lazy = 'joined'
    )