from app.db import db


class Attribute(db.Model):
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
    identifier_code = db.Column(
        db.String(3)
    )
    attribute_value = db.relationship(
        'AttributeValue',
        backref = 'attribute',
        lazy = 'joined'
    )
    
    
    def __init__(self, *args, **kwargs):
        if not in kwargs:
            self.identifier_code = kwargs['name'][0:2].lower()
        super().__init__(*args, **kwargs)