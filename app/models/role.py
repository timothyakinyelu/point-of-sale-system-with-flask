from app.db import db
from .pivots import permission_role_table
from app.perm_helpers import HasPermissionTrait

class Role(db.Model, HasPermissionTrait):
    __tablename__ = 'roles'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(
        db.Integer,
        primary_key = True,
        autoincrement = True
    )
    title = db.Column(
        db.String(100),
        nullable = False
    )
    permissions = db.relationship(
        "Permission", 
        secondary = permission_role_table, 
        backref = "roles", 
        lazy = "joined"
    )
    users = db.relationship(
        "User", 
        backref = "role", 
        lazy = "joined"
    )
    
    
    def __init__(self, title):
        super(Role, self).__init__()
        self.title = title
        
        
    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
           'id': self.id,
           'title': self.title,
           'permissions': self.serialize_permissions
           # This is an example how to deal with Many2Many relations
        }
        
    @property
    def serialize_permissions(self):
        """
        Return object's relations in easily serializable format.
        NB! Calls many2many's serialize property.
        """
        return [ item.serialize for item in self.permissions];