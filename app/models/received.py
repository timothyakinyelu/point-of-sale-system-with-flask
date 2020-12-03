from app.db import db
from flask_sqlalchemy import event
from app.models.product import Product
from datetime import datetime

def dump_datetime(value):
    """Deserialize datetime object into string form for JSON processing."""
    if value is None:
        return None
    d = value.strftime("%Y-%m-%d %H:%M:%S")
    return datetime.strptime(d, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d %I:%M:%S %p")

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
    cost_price = db.Column(
        db.Float
    )
    selling_price = db.Column(
        db.Float
    )
    invoice_number = db.Column(
        db.String(100),
        nullable = False
    )
    date_received  = db.Column(
        db.DateTime,  
        default = db.func.current_timestamp()
    )
    
    @event.listens_for(db.session, 'before_flush')
    def addProductStock(*args):
        sess = args[0]
        for obj in sess.new:
            if not isinstance(obj, Received):
                continue
            
            product = Product.query.filter_by(id = obj.product_id).first()
            product.stock_qty = product.stock_qty + obj.qty_received
            db.session.add(product)
    
    @event.listens_for(db.session, 'before_flush')
    def changeCostPrice(*args):
        sess = args[0]
        for obj in sess.new:
            if not isinstance(obj, Received):
                continue
            
            product = Product.query.filter_by(id = obj.product_id).first()
            product.cost_of_purchase = obj.cost_price
            db.session.add(product)
    
    @event.listens_for(db.session, 'before_flush')
    def changeSellingPrice(*args):
        sess = args[0]
        for obj in sess.new:
            if not isinstance(obj, Received):
                continue
            
            product = Product.query.filter_by(id = obj.product_id).first()
            if obj.selling_price is not None:
                product.old_price = product.price
                product.price = obj.selling_price
                db.session.add(product)
    