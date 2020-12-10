from flask import render_template, redirect, url_for, flash, request, jsonify
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
            return redirect(url_for('auth.getUsers'))
        except AssertionError as exception_message:
            flash('{}'.format(exception_message))

    return render_template(
        'create_user.html', 
        form = form,
        title = 'Create a New User.'
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
        