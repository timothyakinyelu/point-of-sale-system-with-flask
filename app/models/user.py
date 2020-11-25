from app.db import db
from .pivots import permission_user_table
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(
        db.Integer,
        primary_key = True,
        autoincrement = True
    )
    employee_id = db.Column(
        db.Integer,
        db.ForeignKey('employees.id')
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
    shop_id = db.Column(
        db.Integer,
        db.ForeignKey('shops.id')
    )
    status = db.Column(
        db.String(100),
        server_default="PENDING"
    )
    permissions = db.relationship(
        'Permission', 
        secondary = permission_user_table, 
        backref = 'users', 
        lazy = 'joined'
    )
    transactions = db.relationship(
        'Transaction',
        backref = 'user',
        lazy = 'joined'
    )
      
    def set_password(self, password):
        rounds = current_app.config.get('HASH_ROUNDS', 100000)
        self.password = generate_password_hash(password, method='pbkdf2:sha256:{}'.format(rounds))
        
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
           'id': self.id,
           'username': self.username,
           'role': self.role.title,
           'status': self.active
           # This is an example how to deal with Many2Many relations
        }
        
    # @property
    # def serialize_parent(self):
    #     """
    #     Return object's relations in easily serializable format.
    #     NB! Calls many2many's serialize property.
    #     """
    #     if self.parent_id is not None:
    #         return self.parent.serialize