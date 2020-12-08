from app.db import db
from .pivots import permission_user_table
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app
from app.perm_helpers import HasPermissionTrait
from sqlalchemy.orm import validates  
import re

class User(db.Model, UserMixin, HasPermissionTrait):
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
    
    @validates('username')
    def validate_username(self, key, username):
        if not username:
            raise AssertionError('No username provided!')
        
        if User.query.filter(User.username == username).first():
            raise AssertionError('Username is already in use!')
        
        if len(username) < 5 or len(username) > 50:
            raise AssertError('Username must be between 5 and 50 characters')

        return username
    
    def allowed_perms(self, perms):
        """ check if user has permission to carry out action."""

        if self.hasPermissionTo(perms):
            return True
        return False
      
    def set_password(self, password):
        """ generate a hashed password from input string."""
        if not password:
            raise AssertionError('Password not provided')
        
        if not re.match('\d.*[A-Z]|[A-Z].*\d', password):
            raise AssertionError('Password must contain 1 capital letter and 1 number')
        
        if len(password) < 6 or len(password) > 20:
            raise AssertionError('Password must be between 6 and 20 characters')
        
        rounds = current_app.config.get('HASH_ROUNDS', 100000)
        self.password = generate_password_hash(password, method='pbkdf2:sha256:{}'.format(rounds))
        
    def check_password(self, password):
        """ check if hashed password corresponds to database entry."""
        return check_password_hash(self.password, password)
    
    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
           'id': self.id,
           'username': self.username,
           'role': self.role.title,
           'status': self.status
        }