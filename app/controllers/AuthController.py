from flask import render_template, redirect, url_for, flash, request
from flask_login import logout_user, current_user, login_user
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
        return redirect(url_for('auth.index'))
    
    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        
        if user and user.check_password(password = form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('auth.index'))
        flash('Invalid Credentials')
        return redirect(url_for('nonAuth.login'))
    return render_template('login.html', form = form, title = 'Log In')