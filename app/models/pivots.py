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

category_product_table = db.Table('category_product', db.Model.metadata,
    db.Column(
        'category_id',
        db.Integer,
        db.ForeignKey('categories.id')
    ),
    db.Column(
        'product_id',
        db.Integer,
        db.ForeignKey('products.id')
    )                     
)

attribute_product_table = db.Table('attribute_product', db.Model.metadata,
    db.Column(
        'attribute_id',
        db.Integer,
        db.ForeignKey('attributes.id')
    ),
    db.Column(
        'product_id',
        db.Integer,
        db.ForeignKey('products.id')
    )
)