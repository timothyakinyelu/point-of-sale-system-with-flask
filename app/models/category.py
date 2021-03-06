from app.db import db
from slugify import slugify


class Category(db.Model):
    __tablename__ = 'categories'
    
    id = db.Column(
        db.Integer,
        primary_key = True,
        autoincrement = True
    )
    parent_id = db.Column(
        db.Integer,
        db.ForeignKey('categories.id')
    )
    description = db.Column(
        db.Text
    )
    slug = db.Column(
        db.String(100),
        nullable = False
    )
    identifier_code = db.Column(
        db.String(3),
        nullable = False
    )
    children = db.relationship(
        "Category",
        backref = backref('parent', remote_side=[id]),
        lazy = 'joined',
        join_depth = 2
    )
    products = db.relationship(
        'Product',
        secondary = category_product_table,
        backref = 'categories',
        lazy = 'joined'
    )
    
    
    def __init__(self, *args, **kwargs):
        if not in kwargs:
            self.slug = slugify(kwargs['name'])
            self.identifier_code = kwargs['name'][0:2].lower()
        super().__init__(*args, **kwargs)