from app.db import db
from .pivots import category_product_table
from slugify import slugify


class Category(db.Model):
    __tablename__ = 'categories'
    
    id = db.Column(
        db.Integer,
        primary_key = True,
        autoincrement = True
    )
    name = db.Column(
        db.String(100),
        nullable = False
    )
    description = db.Column(
        db.Text
    )
    parent_id = db.Column(
        db.Integer,
        db.ForeignKey('categories.id')
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
        backref = db.backref('parent', remote_side=[id]),
        lazy = 'joined',
        join_depth = 2,
        cascade = 'all, delete'
    )
    products = db.relationship(
        'Product',
        secondary = "category_product",
        backref = 'categories',
        cascade_backrefs=False,
        lazy = 'joined',
        cascade = 'all, delete'
    )
    
    
    def __init__(self, *args, **kwargs):
        if not 'slug' in kwargs:
            self.slug = slugify(kwargs['name'])
        if not 'identifier_code' in kwargs:
            self.identifier_code = kwargs['name'][0:2].lower()
        super().__init__(*args, **kwargs)