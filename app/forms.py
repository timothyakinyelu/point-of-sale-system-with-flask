from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField, PasswordField, RadioField, BooleanField, SelectMultipleField, IntegerField, DecimalField, HiddenField
from wtforms.validators import DataRequired, InputRequired, Length
from app.models.role import Role
from app.models.shop import Shop
from app.models.category import Category


class CreateUserForm(FlaskForm):
    """Create User Form"""

    def __init__(self):
        super().__init__()  # calls the base initialisation and then...
        
        roles = Role.query.all()
        self.role.choices = [(role.id, role.title) for role in roles]
        
        shops = Shop.query.all()
        self.shop.choices = [(0, "select")]+[(shop.id, shop.name) for shop in shops]
    
    employee = HiddenField(
        'Employee',
        validators=None
    )
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
    shop = SelectField(
        'User Shop',
        validators=None,
        coerce=int,
        default=0
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
        'Password',
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
    
class BrandForm(FlaskForm):
    """Brand Creation Form"""

    name = StringField(
        'Brand',
        validators = [InputRequired()]
    )
    submit = SubmitField('Add Brand')

class CategoryForm(FlaskForm):
    """Category Creation Form"""
    
    def __init__(self):
        super().__init__()
        categories = Category.query.all()
        self.parent.choices =[(0, "select")] + [(category.id, category.name) for category in categories]
    
    name = StringField(
        'Name',
        validators = [DataRequired()]
    )
    description = TextAreaField(
        'Description',
        validators=None
    )
    parent = SelectField(
        'Parent Category',
        validate_choice=None,
        coerce=int,
        default=0
    )
    submit = SubmitField('Add Category')
    
class ProductForm(FlaskForm):
    """ Product Creation Form"""
    
    def __init__(self):
        super().__init__()
        categories = Category.query.all()
        self.categories.choices = [(category.id, category.name) for category in categories]
    
    name = StringField(
        'Product Name',
        validators=[InputRequired()]
    )
    sku = StringField(
        'SKU',
        validators=[InputRequired()]
    )
    gtin = StringField(
        'GTIN',
        validators=None
    )
    brandName = StringField(
        'Brand',
        validators=None
    )
    brand = HiddenField(
        'Brand Id',
        validators=None
    )
    categories = SelectMultipleField(
        'Categories',
        validators=[DataRequired()],
        coerce = int
    )
    price = DecimalField(
        'Price',
        validators=[InputRequired()]
    )
    old_price = DecimalField(
        'Old Price',
        validators=None
    )
    cost_of_purchase = DecimalField(
        'Cost of Purchase',
        validators=[InputRequired()]
    )
    discount = StringField(
        'Discount',
        validators=None
    )
    apply_discount = BooleanField(
        'Apply Discount',
        default='',
        validators=None
    )
    stock_qty = IntegerField(
        'Stock Quantity',
        validators=[InputRequired()]
    )
    min_stock_qty = IntegerField(
        'Minimum Stock Quantity',
        validators=[InputRequired()]
    )
    submit = SubmitField('Add Product')
    