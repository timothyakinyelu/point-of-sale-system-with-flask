from flask import render_template, redirect, url_for, flash, request, jsonify
from app.models import *
from app.forms import *
from app.db import session
from app.routes.auth import auth

User = user.User
User_Role = role.Role
Perm = permission.Permission
perm_role = pivots.permission_role_table

def getAllRoles():
    return User_Role.query.all()

def getAllPermissions():
    return Perm.query.all()

""" Controller that handles all system settings and access controls """
def users():
    """ Fetch all users from database."""

    return render_template(
        'users.html'
    )
    
def ajaxFetchUsers():
    """ Fetch all users from db"""
    term = request.args.get('query')
    page = request.args.get('page', 1, type=int)
    
    if term:
        users = User.query.filter(
            User.username.ilike('%' + term + '%'),     
        ).paginate(page, 20, True)
    else:
        users = User.query.paginate(page, 20, True)

    next_url = url_for('auth.fetchUsers', page = users.next_num) \
        if users.has_next else None
        
    prev_url = url_for('auth.fetchUsers', page = users.prev_num) \
        if users.has_prev else None

    return jsonify(results = [i.serialize for i in users.items], next_url = next_url, prev_url = prev_url, current_page = users.page, limit = users.per_page, total = users.total)
    
def roles():
    """ Fetch all system roles from database."""
    
    form = RoleForm()
    
    return render_template('roles.html', form=form, title='Create a User Role')

def ajaxFetchRoles():
    """ Fetch all roles from db"""
    term = request.args.get('query')
    page = request.args.get('page', 1, type=int)
    
    if term:
        roles = Role.query.filter(
            Role.title.ilike('%' + term + '%')
        ).paginate(page, 20, True)
    else:
        roles = Role.query.paginate(page, 20, True)

    next_url = url_for('auth.fetchRoles', page = roles.next_num) \
        if roles.has_next else None
        
    prev_url = url_for('auth.fetchRoles', page = roles.prev_num) \
        if roles.has_prev else None

    return jsonify(results = [i.serialize for i in roles.items], next_url = next_url, prev_url = prev_url, current_page = roles.page, limit = roles.per_page, total = roles.total)

def createRole():
    """ Create new system roles."""
    roles = getAllRoles()
    
    form = RoleForm()

    if not form.title.data[0].isdigit():
        if form.validate_on_submit():
            # do something here
            existing_role = User_Role.query.filter_by(title = form.title.data).first()

            if existing_role is None:
                new_role = User_Role(
                    title = form.title.data
                )
                session.add(new_role)
                session.commit()
                
                flash('Role created Successfully!')
                return redirect(url_for('auth.getRoles'))
            
            flash('Role already exists!')
    flash('Value entered must start with an alphabet!')

    return redirect(url_for('auth.getRoles'))

def updateRole(id):
    form = RoleForm()
    
    if not form.title.data[0].isdigit():
        if form.validate_on_submit():
            session.query(User_Role).filter(User_Role.id == id).update({User_Role.title: form.title.data})
            
            flash('Role updated Successfully!')
            return redirect(url_for('auth.getRoles'))
        
        flash('Unable to update role!')
    flash('Value entered must start with an alphabet!')

    return redirect(url_for('auth.getRoles'))

def removeRole(id):
    Role.query.filter_by(id = id).delete()
    flash('Role deleted Successfully!')
    
    return redirect(url_for('auth.getRoles'))

def permissions():
    """ Fetch all system permissions from database."""
    
    form = PermissionForm()
    roles = getAllRoles()
    permissions = getAllPermissions()
    
    access_role = []
    perms = []
    rights = ()
    
    for role in roles:
        for permission in role.permissions:
            access_role.append(role.id)
            perms.append(permission.id)
    
    rights = list(zip(perms, access_role))
        
    return render_template(
        'permissions.html', 
        form=form, 
        title='Create a Permission.', 
        permissions = permissions, 
        roles = roles, 
        access = rights
    )
    

def createPermission():
    """ Create new system permissions."""
    permissions = getAllPermissions()
    
    form = PermissionForm()
    if not form.name.data[0].isdigit():
        if form.validate_on_submit():
            # do something here
            existing_perm = Perm.query.filter_by(name = form.name.data).first()

            if existing_perm is None:
                new_perm = Perm(
                    name = form.name.data
                )
                session.add(new_perm)
                session.commit()
                
                flash('Permission created Successfully!')
                return redirect(url_for('auth.getPermissions'))
            
            flash('Permission already exists!')
    flash('Value entered must start with an alphabet!')
        
    return redirect(url_for('auth.getPermissions'))


def updatePermission(id):
    form = PermissionForm()
    
    if not form.name.data[0].isdigit():
        if form.validate_on_submit():
            Perm.query.filter_by(id = id).update({Perm.name: form.name.data})

            flash('Permission updated Successfully!')
            return redirect(url_for('auth.getPermissions'))
        
        flash('Unable to update permission!')
    flash('Value entered must start with an alphabet!')

    return redirect(url_for('auth.Permissions'))


def removePermissions():
    """ delete permissions and detach from role relationship """
    Perm.query.filter_by(id = id).delete()
    flash('Permission deleted Successfully!')
    
    return redirect(url_for('auth.getPermissions'))
    

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
                # fix these codes later
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