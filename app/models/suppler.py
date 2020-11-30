from app.db import db
from flask import current_app

class Supplier(db.Model):
    __tablename__ = 'suppliers'
    
    id = db.Column(
        db.Integer,
        primary_key = True,
        autoincrement = True
    )
    name = db.Column(
        db.String(100),
        unique = True,
        nullable = False
    )
    phone_number = db.Column(
        db.String(100)
    )
    email = db.Column(
        db.String(100)
    )
    address = db.Column(
        db.Text
    )
    state = db.Column(
        db.String(100)
    )
    account_number = db.Column(
        db.String(100)
    )
    status = db.Column(
        db.String(100),
        server_default="PENDING"
    )
    
    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
           'id': self.id,
           'name': self.name,
           'phone_number': self.phone_number,
           'email': self.email,
           'state': self.state,
           'account_no.': self.account_number,
           'status': self.status
           # This is an example how to deal with Many2Many relations
        }
        
    # @property
    # def serialize_parent(self):
    #     """
    #     Return object's relations in easily serializable format.
    #     NB! Calls many2many's serialize property.
    #     """
    #     if self.parent_id is not None:
    #         return self.parent.serialize