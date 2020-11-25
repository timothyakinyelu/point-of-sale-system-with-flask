from flask import render_template, redirect, url_for, flash, request
from flask_login import logout_user, current_user, login_user
from is_safe_url import is_safe_url
from app.models import *
from app.forms import *
from app.db import session

User = user.User

""" Controller handle user authentication. """
def authenticate():
    """ checks if user is currently logged in
        and redirects to dashboard. 
        
        if user not logged in sends a POST request to validate user
    """
    
    if current_user.is_authenticated:
        if current_user.status != 'ACTIVE':
            flash('User not yet approved')
            return redirect(url_for('nonAuth.login'))
    
        if current_user.role == 'Cashier':
            return redirect(url_for('auth.addTransaction'))
        return redirect(url_for('auth.dashboard'))
    
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        
        if user.status != 'ACTIVE':
            flash('User not yet approved')
            return redirect(url_for('nonAuth.login'))
        
        if user and user.check_password(password = form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            
            if not is_safe_url('/', next):
                return flask.abort(400)
                
            if user.role_id == 1:
                return redirect(url_for('auth.addTransaction'))
            return redirect(next_page or url_for('auth.dashboard'))
        flash('Invalid Credentials!')
        return redirect(url_for('nonAuth.login'))

   
    return render_template('login.html', form = form, title = 'Log In')