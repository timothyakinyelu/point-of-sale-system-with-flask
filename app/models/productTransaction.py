from flask import current_app
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


class ProductTransaction(db.Model):
    __tablename__ = 'product_transaction'
    
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
    transaction_id = db.Column(
        db.Integer,
        db.ForeignKey('transactions.id'),
        nullable = False
    )
    product_qty = db.Column(
        db.Integer,
        nullable = False
    )
    product = db.relationship(
        'Product',
        backref = 'product_assoc',
        lazy = 'joined'
    )
    transaction = db.relationship(
        'Transaction',
        backref = 'transaction_assoc',
        lazy = 'joined'
    )
    
    
    @event.listens_for(db.session, 'before_flush')
    def reduceProductStock(*args):
        sess = args[0]
        for obj in sess.new:
            if not isinstance(obj, ProductTransaction):
                continue
            
            product = Product.query.filter_by(id = obj.product_id).first()
            product.stock_qty = product.stock_qty - obj.product_qty
            db.session.add(product)
    
    
    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
           'id': self.id,
           'date': dump_datetime(self.transaction.date_created),
           'product': self.product.name,
           'qty_sold': self.product_qty,
           'stock': self.product.stock_qty,
           'cost': "{}{:,.2f}".format(current_app.config['CURRENCY_ICON'], float(self.product.cost_of_purchase)),
        }
