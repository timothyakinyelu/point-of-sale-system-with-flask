from flask_wtf import FlaskForm
from wtforms import StringField, TextField, SubmitField, SelectField, PasswordField, RadioField
from wtforms.validators import DataRequired, InputRequired, Length
from app.models import *

Role = role.Role

"""Create User Form"""
class CreateUserForm(FlaskForm):
    def __init__(self):
        super().__init__()  # calls the base initialisation and then...
        roles = Role.query.all()
        self.role.choices = [(role.id, role.title) for role in roles]
    
    username = StringField(
        'Username',
        validators=[DataRequired()]
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=6, message='Password too short')
        ]
    )
    active = RadioField(
        'Status',
        choices=[('ACTIVE', 'Active'),('PENDING', 'Pending')]
    )
    role = SelectField(
        'User Role',
        validators=[DataRequired()],
        coerce=int
    )
    submit = SubmitField('Create User')
    
"""Login Form"""
class LoginForm(FlaskForm):
    username = StringField(
        'Username',
        validators = [
            DataRequired(),
            Length(min=6, message='Enter a valid username')
        ]
    )
    password = PasswordField(
        'password',
        validators = [DataRequired()]
    )
    submit = SubmitField('Log In')
    
    
"""Role Creation Form"""
class RoleForm(FlaskForm):
    title = StringField(
        'Role',
        validators = [InputRequired()]
    )
    submit = SubmitField('Add Role')
    
"""Permission Creation Form"""
class PermissionForm(FlaskForm):
    name = StringField(
        'Permission',
        validators = [InputRequired()]
    )
    submit = SubmitField('Add Permission')
    