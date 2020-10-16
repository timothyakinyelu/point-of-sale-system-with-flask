from flask import render_template, redirect, url_for, flash, request
from app.models import *
from app.forms import *
from app.db import session
from app.routes.auth import auth

User = user.User
User_Role = role.Role
Perm = permission.Permission
perm_role = pivots.permission_role_table

""" Controller that handles all system settings and access controls """
def users():
    """ Fetch all users from database."""
    
    form = CreateUserForm()
    users = User.query.all()
    return render_template(
        'users.html', 
        users = users, 
        form = form,
        title = 'Create a New User.'
    )
    
def roles():
    """ Fetch all system roles from database."""
    
    form = RoleForm()
    roles = User_Role.query.all()
    
    return render_template('roles.html', form=form, title='Create a User Role', roles = roles)

def createRoles():
    """ Create new system roles."""
    
    form = RoleForm()
    if form.validate_on_submit():
        # do something here
        existing_role = User_Role.query.filter_by(title = form.title.data).first()

        if existing_role is None:
            new_role = User_Role(
                title = form.title.data
            )
            session.add(new_role)
            session.commit()
            return redirect(url_for('auth.getRoles'))
        
        flash('Role already exists')
        # return redirect(url_for('auth.getRoles'))
    return render_template('roles.html')

def permissions():
    """ Fetch all system permissions from database."""
    
    form = PermissionForm()
    roles = User_Role.query.all()
    permissions = Perm.query.all()
    
    access = []
    perms = []
    rights = ()
    
    for role in roles:
        for permission in role.permissions:
            access.append(role.id)
            perms.append(permission.id)
    
    rights = list(zip(perms, access))
        
    return render_template(
        'permissions.html', 
        form=form, 
        title='Create a Permission.', 
        permissions = permissions, 
        roles = roles, 
        access = rights
    ) 

def createPermissions():
    """ Create new system permissions."""
    
    form = PermissionForm()
    if form.validate_on_submit():
        # do something here
        existing_perm = Perm.query.filter_by(name = form.name.data).first()

        if existing_perm is None:
            new_perm = Perm(
                name = form.name.data
            )
            session.add(new_perm)
            session.commit()
            return redirect(url_for('auth.getPermissions'))
        
        flash('Permission already exists')
        # return redirect(url_for('auth.getPermissions'))
    return render_template('permissions.html')

def checkPermissions():
    """
        Check if permission/role relationship exists in database.
        if it does not, create new permission/role relationship.
        
        if unchecked revoke permissions given to role
    """
    
    if request.method == 'POST':
        access = {}
        revoked = {}
        selected = []
        unselected = []
        
        values = [tuple(map(int, value.split('-'))) for value in request.form.getlist('check')]
        checked = 'check' in request.form
        heads = ['permission', 'role']
        
        access_roles = session.query(perm_role).all()
        
        # check if checked values are already in db before adding
        for x in values:
            if x not in access_roles:
                selected.append(x)
                
        for items in selected:
            access = dict(zip(heads, items))

            if selected:
                role = User_Role.query.filter_by(id = access['role']).first()
                perms = Perm.query.filter_by(id = access['permission']).all()
                
                role.givePermissionsTo(perms)
        
        # check if box is unselected and revoke permission in db
        for x in access_roles:
            if x not in values:
                unselected.append(x)
        
        for i in unselected:
            revoked = dict(zip(heads, i))  
        
            if unselected:
                xRole = User_Role.query.filter_by(id = revoked['role']).first()
                xPerms = Perm.query.filter_by(id = revoked['permission']).all()
                
                xRole.revokePermissions(xPerms)
            
        return redirect(url_for('auth.getPermissions'))