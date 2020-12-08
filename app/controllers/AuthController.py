from flask import render_template, redirect, url_for, flash, request
from flask_login import logout_user, current_user, login_user
from is_safe_url import is_safe_url
from app.models import *
from app.forms import *
from app.db import session
import logging
import logging.config
from os import path

User = user.User
log_file_path = path.abspath('logging.conf')
logging.config.fileConfig(log_file_path, disable_existing_loggers=False)
logger = logging.getLogger(__name__)

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
    
        if current_user.allowed_perms(['enter-sales']):
            return redirect(url_for('auth.addTransaction'))
        
        if current_user.allowed_perms(['view-dashboard']):
            return redirect(url_for('auth.dashboard'))
    
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        
        if user is not None:
            if user.status != 'ACTIVE':
                flash('User not yet approved')
                return redirect(url_for('nonAuth.login'))
            
            if user and user.check_password(password = form.password.data):
                login_user(user)
                next_page = request.args.get('next')
                
                if not is_safe_url('/', next):
                    return flask.abort(400)
                    
                if user.allowed_perms(['enter-sales']):
                    logger.info(user.username + ' ' + 'successful Log In')
                    return redirect(url_for('auth.addTransaction'))
                elif user.allowed_perms(['view-dashboard']):
                    logger.info(user.username + ' ' + 'successful Log In')
                    return redirect(next_page or url_for('auth.dashboard'))
                else:
                    logger.warn(user.username + ' ' + 'has no permissions')

            logger.warn(user.username + ' ' + 'Failed login attempt')
            
        logger.warn(' Unknown user failed login attempt')
        flash('Invalid Credentials!')
        return redirect(url_for('nonAuth.login'))

   
    return render_template('login.html', form = form, title = 'Log In')