from flask import render_template, redirect, url_for
from . import auth
from app.controllers import SystemController
from app.controllers import UserController
from flask_login import login_required, logout_user

@auth.route('/')
@login_required
def index():
    return render_template('index.html')

@auth.route('/system/users')
@login_required
def getUsers(): 
    return SystemController.users()

@auth.route('/system/users/create-new-user', methods=['GET', 'POST'])
@login_required
def createUser():
    return UserController.create()

@auth.route('/system/roles')
@login_required
def getRoles():
    return SystemController.roles()

@auth.route('/system/roles/create-role', methods=['POST',])
@login_required
def createRole():
    return SystemController.createRoles()
  
@auth.route('/system/permissions')
@login_required
def getPermissions():
    return SystemController.permissions()

@auth.route('/system/permissions/create-permission', methods=['POST',])
@login_required
def createPermission():
    return SystemController.createPermissions()
            
@auth.route('/system/permissions/check-permission', methods=['POST',])
@login_required
def checkPerm():
    return SystemController.checkPermissions()

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('nonAuth.login'))