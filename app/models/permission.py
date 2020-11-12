from app.db import db
from slugify import slugify

class Permission(db.Model):
    __tablename__ = 'permissions'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(
        db.Integer,
        primary_key = True,
        autoincrement = True
    )
    name = db.Column(
        db.String(100),
        nullable = False
    )
    slug = db.Column(
        db.String(100),
        nullable = False
    )
    
    
    def __init__(self, *args, **kwargs):
        if not 'slug' in kwargs:
            self.slug = slugify(kwargs['name'])
        super().__init__(*args, **kwargs)
        
        
    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
           'id': self.id,
           'name': self.name,
           'slug': self.slug
           # This is an example how to deal with Many2Many relations
        }