from flask import render_template, redirect, url_for, flash, request
from app.models import *
from app.forms import *
from . import nonAuth
from app.db import session

User_Roles = role.Role
Perms = permission.Permission
perm_role = pivots.permission_role_table

# def getRoles():
#     sys_roles = User_Roles.query.all()
#     return sys_roles
    
# def getPermissions():
#     permissions = Perms.query.all()
#     return permissions

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
    roles = User_Roles.query.all()
    permissions = Perms.query.all()
    
    access = []
    perms = []
    rights = ()
    
    for role in roles:
        for permission in role.permissions:
            access.append(role.id)
            perms.append(permission.id)
    
    rights = list(zip(perms, access))
        
    return render_template('permissions.html', form=form, title='Create a Permission', permissions = permissions, roles = roles, access = rights)  

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


# @nonAuth.route('/system/permissions/check-permission/<int:roleID>/<int:permID>', methods=['POST',])
# def checkPerm(roleID, permID):
#     if request.method == 'POST':
#         role = User_Roles.query.filter_by(id = roleID).first()
#         perm = Perms.query.filter_by(id = permID).first()
        
#         checked = 'check' in request.form
        
#         if checked == True:
#             role.givePermissionsTo(perm)
#         else:
#             role.revokePermissions(permID)
            
@nonAuth.route('/system/permissions/check-permission', methods=['POST',])
def checkPerm():
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
                role = User_Roles.query.filter_by(id = access['role']).first()
                perms = Perms.query.filter_by(id = access['permission']).all()
                
                role.givePermissionsTo(perms)
        
        # check if box is unselected and revoke permission in db
        for x in access_roles:
            if x not in values:
                unselected.append(x)
        
        for i in unselected:
            revoked = dict(zip(heads, i))  
        
            if unselected:
                xRole = User_Roles.query.filter_by(id = revoked['role']).first()
                xPerms = Perms.query.filter_by(id = revoked['permission']).all()
                
                xRole.revokePermissions(xPerms)
            
        return redirect(url_for('nonAuth.getPermissions'))