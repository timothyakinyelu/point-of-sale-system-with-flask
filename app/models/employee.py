from app.db import db

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
    