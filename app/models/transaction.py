from app.db import db


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
    date_created  = db.Column(
        db.DateTime,  
        default = db.func.current_timestamp()
    )