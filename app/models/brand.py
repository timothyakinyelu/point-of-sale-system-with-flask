from app.db import db
from slugify import slugify


class Brand(db.Model):
    __table__name = 'brands'
    
    id = db.Column(
        db.Integer,
        primary_key = True,
        autoincrement = True
    )
    name = db.Column(
        db.String(100),
        nullable = False
    )
    slug = db.Column(
        db.String(100),
        nullable = False
    )
    identifier_code = db.Column(
        db.String(3),
        nullable = False
    )
    products = db.relationship(
        'Product',
        backref = 'brand',
        lazy = 'joined'
    )
    
    
    def __init__(self, *args, **kwargs):
        if not in kwargs:
            self.slug = slugify(kwargs['name'])
            self.identifier_code = kwargs['name'][0:2].lower()
        super().__init__(*args, **kwargs)