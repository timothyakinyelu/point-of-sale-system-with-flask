from app.db import db
from flask_sqlalchemy import event
from app.models.product import Product


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
            
            product = Products.query.filter_by(id = obj.product_id).first()
            product.stock_qty = product.stock_qty - obj.product_qty
            db.session.add(product)
    
    