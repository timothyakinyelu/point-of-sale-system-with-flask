from flask import render_template, redirect, url_for, flash
from app.models import *
from app.forms import *
from . import nonAuth
from app.db import session

User_Roles = role.Role
Perms = permission.Permission

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
        
        flash('Role already exists')
        return redirect(url_for('nonAuth.getRoles'))

    
@nonAuth.route('/system/permissions')
def getPermissions():
    form = PermissionForm()
    
    permissions = Perms.query.all()
    return render_template('permissions.html', form=form, title='Create a Permission', permissions = permissions)

@nonAuth.route('/system/permissions/create-permission', methods=['POST',])
def createPermission():
    form = PermissionForm()
    if form.validate_on_submit():
        print(form.name.data)
        # do something here
        existing_perm = Perms.query.filter_by(name = form.name.data).first()

        if existing_perm is None:
            new_perm = Perms(
                name = form.name.data
            )
            session.add(new_perm)
            session.commit()
            return redirect(url_for('nonAuth.getPermissions'))
        
        flash('Permission already exists')
        return redirect(url_for('nonAuth.getPermissions'))
