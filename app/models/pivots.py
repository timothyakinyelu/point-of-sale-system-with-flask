from app.db import db

role_user_table = db.Table('role_user',
  db.Column('user_id', db.Integer(), 
  db.ForeignKey('users.id')),
  db.Column('role_id', db.Integer(), 
  db.ForeignKey('roles.id')))

permission_user_table = db.Table('permission_user',
  db.Column('permission_id', db.Integer(), 
  db.ForeignKey('permissions.id')),
  db.Column('user_id', db.Integer(), 
  db.ForeignKey('users.id')))

permission_role_table = db.Table('permission_role',
  db.Column('permission_id', db.Integer(), 
  db.ForeignKey('permissions.id')),
  db.Column('role_id', db.Integer(), 
  db.ForeignKey('roles.id')))