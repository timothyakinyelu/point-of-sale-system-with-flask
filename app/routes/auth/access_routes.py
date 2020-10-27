from flask import render_template, redirect, url_for
from . import auth
from app.controllers import SystemController
from app.controllers import UserController
from app.controllers import ShopController
from app.controllers import BrandController
from app.controllers import CategoryController
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

@auth.route('/system/roles/update-role/<int:id>', methods=['POST',])
@login_required
def updateRole(id):
    return SystemController.updateRoles(id)

@auth.route('/system/roles/delete-role/<int:id>', methods=['POST',])
@login_required
def deleteRole(id):
    return SystemController.deleteRoles(id)
  
@auth.route('/system/permissions')
@login_required
def getPermissions():
    return SystemController.permissions()

@auth.route('/system/permissions/create-permission', methods=['POST',])
@login_required
def createPermission():
    return SystemController.createPermissions()

@auth.route('/system/permissions/update-permission/<int:id>', methods=['POST',])
@login_required
def updatePermission(id):
    return SystemController.updatePermissions(id)

@auth.route('/system/permissions/delete-permission/<int:id>', methods=['POST',])
@login_required
def deletePermission(id):
    return SystemController.deletePermissions(id)
            
@auth.route('/system/permissions/check-permission', methods=['POST',])
@login_required
def checkPerm():
    return SystemController.checkPermissions()

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('nonAuth.login'))


# Main shop routes
@auth.route('/system/shops')
@login_required
def getShops():
    return ShopController.shops()

@auth.route('/system/shops/create-shop', methods=['POST',])
@login_required
def createShop():
    return ShopController.createShops()

@auth.route('/system/shops/update-shop/<int:id>', methods=['POST',])
@login_required
def updateShop(id):
    return ShopController.updateShops(id)

@auth.route('/system/shops/delete-shop/<int:id>', methods=['POST',])
@login_required
def deleteShop(id):
    return ShopController.deleteShops(id)

@auth.route('/system/brands')
@login_required
def getBrands():
    return BrandController.brands()

@auth.route('/system/brands/create-brand', methods=['POST',])
@login_required
def createBrand():
    return BrandController.createBrands()

@auth.route('/system/brands/update-brand/<int:id>', methods=['POST',])
@login_required
def updateBrand(id):
    return BrandController.updateBrands(id)

@auth.route('/system/brands/delete-brand/<int:id>', methods=['POST',])
@login_required
def deleteBrand(id):
    return BrandController.deleteBrands(id)

@auth.route('/system/categories')
@login_required
def getCategories():
    return CategoryController.categories()

@auth.route('/system/categories/create-category', methods=['POST',])
@login_required
def createCategory():
    return CategoryController.createCategories()

@auth.route('/system/categories/update-category/<int:id>', methods=['POST',])
@login_required
def updateCategory(id):
    return CategoryController.updateCategories(id)

@auth.route('/system/categories/delete-category/<int:id>', methods=['POST',])
@login_required
def deleteCategory(id):
    return CategoryController.deleteCategories(id)