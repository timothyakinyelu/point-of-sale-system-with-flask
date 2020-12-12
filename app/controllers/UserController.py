from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import current_user
from app.models import *
from app.forms import *
from app.db import session
from sqlalchemy import func
import logging
import logging.config
from os import path


log_file_path = path.abspath('logging.conf')
logging.config.fileConfig(log_file_path, disable_existing_loggers=False)
logger = logging.getLogger(__name__)

User = user.User
Employee = employee.Employee

def create():
    """ Create a new user access to the system."""
    
    form = CreateUserForm()
    if form.validate_on_submit():
        try:
            user = User(
                username = form.username.data,
                status = form.status.data,
                role_id = form.role.data,
                employee_id = None if form.employee.data == '' else form.employee.data,
                shop_id = None if form.shop.data == 0 else form.shop.data
            )
            
            user.set_password(form.password.data)
            session.add(user)
            session.commit()
            
            flash('User created Successfully!')
            return redirect(url_for('auth.getUsers'))
        except AssertionError as exception_message:
            flash('{}'.format(exception_message))

    return render_template(
        'create_user.html', 
        form = form,
        data_type = 'New User', 
        form_action=url_for('auth.createUser'),
        action = 'Add',
    )
    
def updateUser(user_id):
    """ Update existing user in db"""
   
    user = User.query.filter_by(id = user_id).first()
    form = CreateUserForm()
    if request.method == 'GET':
        form.username.data = user.username
        form.role.data = user.role_id
        form.employee.data = user.employee_id
        form.shop.data = user.shop_id
        form.status.data = user.status
    
    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                updatedUser = session.query(User).filter(User.id == user_id).update({
                    User.username: form.username.data,
                    User.status: form.status.data,
                    User.role_id: form.role.data,
                    User.employee_id: None if form.employee.data == '' else form.employee.data,
                    User.shop_id: None if form.shop.data == 0 else form.shop.data
                })
                
                updateUser.set_password(form.password.data)
                session.commit()
                
                flash('User updated Successfully!')
                return redirect(url_for('auth.getUsers'))
            except AssertionError as exception_message:
                flash('{}'.format(exception_message))
        
        flash('Unable to update user!')
    return render_template(
        'create_user.html',
        form = form, 
        data_type = user.username, 
        form_action=url_for('auth.updateUser', user_id = user.id),
        action = 'Edit',
    )

    
def searchEmployees():
    term = request.args.get('query')
    records = Employee.query.filter(Employee.first_name.ilike('%' + term + '%')).all()
    
    return jsonify(results = [i.serialize for i in records])

def removeUser():
    """ delete users form db"""
    
    if request.method == 'POST':
        ids = request.json['selectedIDs']
        
        session.query(User).filter(User.id.in_(ids)).delete(synchronize_session=False)
        session.commit()
        
        data = {'message': 'User(s) deleted Successfully!', 'status': 200}
        logger.warn(current_user.username + ' ' + 'deleted user(s)')
        return make_response(jsonify(data), 200)
        