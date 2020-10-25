from app.db import db


class Discount(db.Model):
    __tablename__ = 'discounts'
    
    id = db.Column(
        db.Integer,
        primary_key = True,
        autoincrement = True
    )
    name = db.Column(
        db.String(50)
        nullable = False
    )
    discount_type = db.Column(
        db.String(50)
    )
    amount = db.Column(
        db.Float
        nullable = False
    )
    requires_coupon = db.Column(
        db.Boolean,
        server_default="0"
    )
    start_date  = db.Column(
        db.Date
    )
    end_date  = db.Column(
        db.Date
    )
    products = db.relationship(
        'Product',
        backref = 'discount',
        lazy = 'joined'
    )