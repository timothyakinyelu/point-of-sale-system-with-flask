from app.db import db


def dump_datetime(value):
    """Deserialize datetime object into string form for JSON processing."""
    if value is None:
        return None
    return value.strftime("%Y-%m-%d")

class Employee(db.Model):
    __tablename__ = 'employees'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(
        db.Integer,
        primary_key = True,
        autoincrement = True
    )
    first_name = db.Column(
        db.String(100),
        nullable = False
    )
    last_name = db.Column(
        db.String(100),
        nullable = False
    )
    email = db.Column(
        db.String(100)
    )
    phone_number = db.Column(
        db.String(100),
        nullable = False
    )
    address = db.Column(
        db.Text,
        nullable = False
    )
    referee = db.Column(
        db.String(100)
    )
    salary = db.Column(
        db.String(100)
    )
    position = db.Column(
        db.String(100)
    )
    date_of_birth = db.Column(
        db.DateTime
    )
    date_hired = db.Column(
        db.DateTime
    )
    users = db.relationship(
        "User", 
        backref = "employee", 
        lazy = "joined"
    )
    
    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
           'id': self.id,
           'first_name': self.first_name,
           'last_name': self.last_name,
           'date_of_birth': dump_datetime(self.date_of_birth),
           'date_hired': dump_datetime(self.date_hired),
           # This is an example how to deal with Many2Many relations
        }
       
    # @property
    # def serialize_many2many(self):
    #    """
    #    Return object's relations in easily serializable format.
    #    NB! Calls many2many's serialize property.
    #    """
    #    return [ item.serialize for item in self.many2many]