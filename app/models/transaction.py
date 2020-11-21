from flask import current_app
from app.db import db
from datetime import datetime


def dump_datetime(value):
    """Deserialize datetime object into string form for JSON processing."""
    if value is None:
        return None
    d = value.strftime("%Y-%m-%d %H:%M:%S")
    return datetime.strptime(d, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d %I:%M:%S %p")

class Transaction(db.Model):
    __tablename__ = 'transactions'
    
    id = db.Column(
        db.Integer,
        primary_key = True,
        autoincrement = True
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable = False
    )
    shop_id = db.Column(
        db.Integer,
        db.ForeignKey('shops.id'),
        nullable = False,
    )
    payment_method = db.Column(
        db.String(50),
        nullable = False,
        server_default="CASH"
    )
    pos_ref_number = db.Column(
        db.String(100)
    )
    amount = db.Column(
        db.Float
    )
    cost = db.Column(
        db.Float
    )
    date_created  = db.Column(
        db.DateTime,  
        default = db.func.current_timestamp()
    )
    
    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
           'id': self.id,
           'date': dump_datetime(self.date_created),
           'user': self.serialize_user,
           'shop': self.serialize_shop,
           'payment_type': self.payment_method,
           'pos_ref_number': self.pos_ref_number,
           'total': "{}{:,.2f}".format(current_app.config['CURRENCY_ICON'], float(self.amount)),
        }
        
    @property
    def serialize_shop(self):
        """
        Return object's relations in easily serializable format.
        NB! Calls one2many serialize property.
        """
        if self.shop_id is not None:
            return self.shop.name
        return None
    
    @property
    def serialize_user(self):
        return self.user.username