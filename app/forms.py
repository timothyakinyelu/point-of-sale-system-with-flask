from flask_wtf import FlaskForm
from wtforms import StringField, TextField, SubmitField, SelectField, PasswordField, RadioField
from wtforms.validators import DataRequired, Length

"""Create User Form"""
class CreateUserForm(FlaskForm):
    selection_field = SelectField()
    def __init__(self):
        super(CreateUserForm, self).__init__()
        
        from app.models.role import Role
        self.selection_field.choices = Role.query.all()
        
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
        'Active User',
        validators=[DataRequired()]
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
        validators = [DataRequired()]
    )
    submit = SubmitField('Add Role')
    
"""Permission Creation Form"""
class PermissionForm(FlaskForm):
    name = StringField(
        'Permission',
        validators = [DataRequired()]
    )
    submit = SubmitField('Add Permission')
    