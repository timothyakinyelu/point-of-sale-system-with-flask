from flask import render_template, redirect, url_for, flash
from app.models import *
from app.forms import *
from app.db import session

User = user.User

def create():
    """ Create a new user access to the system."""
    
    form = CreateUserForm()
    
    if form.validate_on_submit():
        
        existing_user = User.query.filter_by(username = form.username.data).first()
        
        if existing_user is None:
            user = User(
                username = form.username.data,
                active = form.active.data,
                role_id = form.role.data
            )
            user.set_password(form.password.data)
            session.add(user)
            session.commit()
            
            return redirect(url_for('auth.getUsers'))
        flash('User already exists')
    return render_template(
        'users.html', 
        form = form,
        title = 'Create a New User.'
    )