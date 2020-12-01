from app.db import db

class Received(db.Model):
    __tablename__ = 'received'
    
    id = db.Column(
        db.Integer,
        primary_key = True,
        autoincrement = True
    )
    product_id = db.Column(
        db.Integer,
        db.ForeignKey('products.id'),
        nullable = False
    )
    supplier_id = db.Column(
        db.Integer,
        db.ForeignKey('suppliers.id'),
        nullable = False
    )
    qty_received = db.Column(
       db.Integer
    )
    invoice_number = db.Column(
        db.String(100),
        nullable = False
    )
    date_received  = db.Column(
        db.DateTime,  
        default = db.func.current_timestamp()
    )
    