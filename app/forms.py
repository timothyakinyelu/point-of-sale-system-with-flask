from flask_wtf import FlaskForm
from wtforms import StringField, TextField, SubmitField, SelectField, PasswordField, RadioField
from wtforms.validators import DataRequired, InputRequired, Length
from app.models.role import Role


class CreateUserForm(FlaskForm):
    """Create User Form"""

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
    
class LoginForm(FlaskForm):
    """Login Form"""

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
    
    
class RoleForm(FlaskForm):
    """Role Creation Form"""

    title = StringField(
        'Role',
        validators = [InputRequired()]
    )
    submit = SubmitField('Add Role')
    
class PermissionForm(FlaskForm):
    """Permission Creation Form"""

    name = StringField(
        'Permission',
        validators = [InputRequired()]
    )
    submit = SubmitField('Add Permission')
    
class ShopForm(FlaskForm):
    """Shop Creation Form"""

    name = StringField(
        'Shop',
        validators = [InputRequired()]
    )
    submit = SubmitField('Add Shop')
    