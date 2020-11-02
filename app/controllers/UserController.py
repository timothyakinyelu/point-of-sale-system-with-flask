from flask import render_template, redirect, url_for, flash, request, jsonify
from app.models import *
from app.forms import *
from app.db import session
from sqlalchemy import func

User = user.User
Employee = employee.Employee

def create():
    """ Create a new user access to the system."""
    
    form = CreateUserForm()
    
    if form.validate_on_submit():
        existing_user = User.query.filter_by(username = form.username.data).first()
        
        if existing_user is None:
            user = User(
                username = form.username.data,
                active = form.active.data,
                role_id = form.role.data,
                employee_id = None if form.employee.data == '' else form.employee.data,
                shop_id = None if form.shop.data == 0 else form.shop.data
            )
            user.set_password(form.password.data)
            session.add(user)
            session.commit()
            
            return redirect(url_for('auth.getUsers'))
        flash('User already exists')

    return render_template(
        'create_user.html', 
        form = form,
        title = 'Create a New User.'
    )
    
def searchEmployees():
    term = request.args.get('query')
    records = Employee.query.filter(Employee.first_name.ilike('%' + term + '%')).all()
    
    return jsonify(results = [i.serialize for i in records])
        