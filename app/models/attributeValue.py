from app.db import db


class AttributeValue(db.Model):
    __tablename__ = 'attribute_values'
    
    id = db.Column(
        db.Integer,
        primary_key = True,
        autoincrement = True
    )
    name = db.Column(
        db.String(50),
        nullable = False
    )
    attribute_id = db.Column(
        db.Integer,
        db.ForeignKey('attributes.id'),
        nullable = False
    )
    price_adjustment = db.Column(
        db.Float
    )