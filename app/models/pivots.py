from app.db import db

permission_user_table = db.Table('permission_user', db.Model.metadata,
    db.Column(
        'permission_id', 
        db.Integer, 
        db.ForeignKey('permissions.id')
    ),
    db.Column(
        'user_id', 
        db.Integer, 
        db.ForeignKey('users.id')
    )
)

permission_role_table = db.Table('permission_role', db.Model.metadata,
    db.Column(
        'permission_id', 
        db.Integer, 
        db.ForeignKey('permissions.id')
    ),
    db.Column(
        'role_id', 
        db.Integer, 
        db.ForeignKey('roles.id')
    )
)