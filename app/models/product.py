from app.db import db
from sqlalchemy import func

# class MixinSearch:

#     @classmethod
#     def fulltext_search(cls, session, search_string, field, page):
#         return session.query(cls). \
#             filter(func.to_tsvector('english', getattr(cls, field)).match(search_string, postgresql_regconfig='english')).paginate(page, 1, True)
            
class Product(db.Model):
    __tablename__ = 'products'
    
    id = db.Column(
        db.Integer,
        primary_key = True,
        autoincrement = True
    )
    name = db.Column(
        db.String(100),
        nullable = False
    )
    sku = db.Column(
        db.String(50),
        nullable = False
    )
    gtin = db.Column(
        db.String(50)
    )
    brand_id = db.Column(
        db.Integer,
        db.ForeignKey('brands.id'),
        nullable = False
    )
    price = db.Column(
        db.Float,
        nullable = False
    )
    old_price = db.Column(
        db.Float
    )
    cost_of_purchase = db.Column(
        db.Float
    )
    discount_id = db.Column(
        db.Integer,
        db.ForeignKey('discounts.id')
    )
    has_discount_applied = db.Column(
        db.Boolean,
        server_default = "0"
    )
    stock_qty = db.Column(
        db.Integer
    )
    min_stock_qty = db.Column(
        db.Integer
    )
    date_created  = db.Column(
        db.DateTime,  
        default = db.func.current_timestamp()
    )
    date_modified = db.Column(
        db.DateTime,  
        default = db.func.current_timestamp(),
        onupdate = db.func.current_timestamp()
    )
    
    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
           'id': self.id,
           'sku': self.sku,
           'product': self.name,
           'price': self.price,
           'cost_price': self.cost_of_purchase,
           'discount_id':self.discount_id,
           'discount': self.serialize_discount,
           'stock': self.stock_qty,
           'min_stock': self.min_stock_qty
           # This is an example how to deal with Many2Many relations
        }
        
    @property
    def serialize_discount(self):
        """
        Return object's relations in easily serializable format.
        NB! Calls many2many's serialize property.
        """
        if self.discount_id is not None:
            return self.discount.serialize
        return None