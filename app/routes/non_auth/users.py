from flask import render_template, redirect, url_for, flash
from app.models import *
from app.forms import *
from . import nonAuth
from app.db import session

User_Roles = roles.Roles

@nonAuth.route('/login')
def login():
    return render_template('login.html')

@nonAuth.route('/create-new-user')
def createUser():
    return render_template('create_user.html')

@nonAuth.route('/system/roles')
def getRoles():
    form = RoleForm()
    
    roles = User_Roles.query.all()
    return render_template('roles.html', form=form, title='Create a User Role', roles = roles)

@nonAuth.route('/system/roles/create-role', methods=['POST',])
def createRole():
    form = RoleForm()
    if form.validate_on_submit():
        # do something here
        existing_role = User_Roles.query.filter_by(title = form.title.data).first()

        if existing_role is None:
            new_role = User_Roles(
                title = form.title.data
            )
            session.add(new_role)
            session.commit()
            return redirect(url_for('nonAuth.getRoles'))
        print(existing_role)
        flash('Role already exists')
        return redirect(url_for('nonAuth.getRoles'))
    # return render_template('roles.html', form = form, title='Create a User Role')