from flask import render_template, redirect, url_for
from . import auth
from app.controllers import SystemController
from app.controllers import UserController
from app.controllers import ShopController
from app.controllers import BrandController
from app.controllers import CategoryController
from app.controllers import ProductController
from app.controllers import TransactionController
from app.controllers import DashboardController
from app.controllers import ReportsController
from app.controllers import ReportsController
from app.controllers import SuppliersController
from flask_login import login_required, logout_user
from app.config_helper import required_permissions


@auth.route("/")
@login_required
@required_permissions('view-dashboard')
def dashboard():
    return DashboardController.dashboard()

@auth.route("/chart")
@login_required
def fetchChart():
    return DashboardController.chart()

@auth.route('/settings/users')
@login_required
@required_permissions('view-users')
def getUsers(): 
    return SystemController.users()

@auth.route('/users')
@login_required
def fetchUsers():
    return SystemController.ajaxFetchUsers()

@auth.route('/settings/users/create-new-user', methods=['GET', 'POST'])
@login_required
def createUser():
    return UserController.create()

@auth.route('/settings/roles')
@login_required
@required_permissions('view-roles')
def getRoles():
    return SystemController.roles()

@auth.route('/roles')
@login_required
def fetchRoles():
    return SystemController.ajaxFetchRoles()

@auth.route('/settings/roles/add-role', methods=['POST',])
@login_required
def addRole():
    return SystemController.createRole()

@auth.route('/settings/roles/update-role/<int:id>', methods=['POST',])
@login_required
def updateRole(id):
    return SystemController.updateRole(id)

@auth.route('/settings/roles/delete-role/<int:id>', methods=['POST',])
@login_required
def deleteRole(id):
    return SystemController.removeRole(id)
  
@auth.route('/settings/permissions')
@login_required
@required_permissions('view-permissions')
def getPermissions():
    return SystemController.permissions()

@auth.route('/settings/permissions/add-permission', methods=['POST',])
@login_required
def addPermission():
    return SystemController.createPermission()

@auth.route('/settings/permissions/update-permission/<int:id>', methods=['POST',])
@login_required
def updatePermission(id):
    return SystemController.updatePermission(id)

@auth.route('/settings/permissions/delete-permission', methods=['POST',])
@login_required
def deletePermissions():
    return SystemController.removePermissions()
            
@auth.route('/settings/permissions/check-permission', methods=['POST',])
@login_required
def checkPerm():
    return SystemController.checkPermissions()

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('nonAuth.login'))


# Main shop routes
@auth.route('/settings/shops')
@login_required
@required_permissions('view-shops')
def getShops():
    return ShopController.shops()

@auth.route('/shops')
@login_required
def fetchShops():
    return ShopController.ajaxFetchShops()

@auth.route('/settings/shops/add-shop', methods=['POST',])
@login_required
def addShop():
    return ShopController.createShop()

@auth.route('/settings/shops/update-shop/<int:id>', methods=['POST',])
@login_required
def updateShop(id):
    return ShopController.updateShop(id)

@auth.route('/settings/shops/delete-shop/<int:id>', methods=['POST',])
@login_required
def deleteShop(id):
    return ShopController.removeShop(id)

@auth.route('/inventory/brands')
@login_required
@required_permissions('view-brands')
def getBrands():
    return BrandController.brands()

@auth.route('/brands')
@login_required
def fetchBrands():
    return BrandController.ajaxFetchBrands()

@auth.route('/inventory/brands/add-brand', methods=['POST',])
@login_required
def addBrand():
    return BrandController.createBrand()

@auth.route('/inventory/brands/update-brand/<int:id>', methods=['POST',])
@login_required
def updateBrand(id):
    return BrandController.updateBrand(id)

@auth.route('/inventory/brands/delete-brand/<int:id>', methods=['POST',])
@login_required
def deleteBrand(id):
    return BrandController.removeBrand(id)

@auth.route('/inventory/categories')
@login_required
@required_permissions('view-categories')
def getCategories():
    return CategoryController.categories()

@auth.route('/categories')
@login_required
def fetchCategories():
    return CategoryController.ajaxFetchCategories()

@auth.route('/inventory/categories/add-category', methods=['POST',])
@login_required
def addCategory():
    return CategoryController.createCategory()

@auth.route('/inventory/categories/update-category/<int:id>', methods=['POST',])
@login_required
def updateCategory(id):
    return CategoryController.updateCategory(id)

@auth.route('/inventory/categories/delete-category/<int:id>', methods=['POST',])
@login_required
def deleteCategory(id):
    return CategoryController.removeCategory(id)

@auth.route('/inventory/suppliers')
@login_required
@required_permissions('view-products')
def getSuppliers():
    return SuppliersController.suppliers()

@auth.route('/suppliers')
@login_required
def fetchSuppliers():
    return SuppliersController.ajaxFetchSuppliers()

@auth.route('/inventory/suppliers/add-supplier', methods=['GET', 'POST'])
@login_required
def addSupplier():
    return SuppliersController.createSupplier()

@auth.route('/inventory/suppliers/update-supplier/<int:id>', methods=['GET', 'POST'])
@login_required
def updateSupplier(id):
    return SuppliersController.updateSupplier(id)

@auth.route('/inventory/suppliers/delete-supplier/<int:id>', methods=['POST',])
@login_required
def deleteSupplier(id):
    return SuppliersController.removeSupplier(id)

@auth.route('/inventory/products')
@login_required
@required_permissions('view-products')
def getProducts():
    return ProductController.products()

@auth.route('/products')
@login_required
def fetchProducts():
    return ProductController.ajaxFetchProducts()

@auth.route('/inventory/products/add-product', methods=['GET', 'POST'])
@login_required
def addProduct():
    return ProductController.createProduct()

@auth.route('/inventory/products/update-product/<int:id>', methods=['GET', 'POST'])
@login_required
def updateProduct(id):
    return ProductController.updateProduct(id)

@auth.route('/inventory/products/delete-product/<int:id>', methods=['POST',])
@login_required
def deleteProduct(id):
    return ProductController.removeProduct(id)

@auth.route('/sales/new-transaction')
@login_required
@required_permissions('enter-sales')
def addTransaction():
    return TransactionController.new_transaction()

@auth.route('/sales/submit-transaction', methods=['POST',])
@login_required
def submitTransaction():
    return TransactionController.submit_transaction()

@auth.route('/search-employees')
@login_required
def searchEmployees():
    return UserController.searchEmployees()

@auth.route('/search-brands')
@login_required
def searchBrands():
    return ProductController.searchBrands()

@auth.route('/get-product')
@login_required
def getProduct():
    return ProductController.getProduct()

@auth.route('/reports/sales-report')
@login_required
@required_permissions('view-reports')
def salesReport():
    return ReportsController.salesReports()

@auth.route('/sales-report')
@login_required
def fetchSalesReport():
    return ReportsController.allSalesReport()

@auth.route('/reports/products-report')
@login_required
@required_permissions('view-reports')
def productsReport():
    return ReportsController.productsReports()

@auth.route('/products-report')
@login_required
def fetchProductsReport():
    return ReportsController.allProductsReport()

@auth.route('/reports/low-stock')
@login_required
@required_permissions('view-low-stock')
def lowStockReport():
    return ReportsController.lowStocksReport()

@auth.route('/low-stock')
@login_required
def fetchLowStocks():
    return ReportsController.allLowStocks()

@auth.route('/reports/today-sales')
@login_required
@required_permissions('view-day-report')
def todaysReport():
    return ReportsController.salesByCurrentDate()

@auth.route('/today-sales')
@login_required
def fetchTodaySales():
    return ReportsController.getTodaySales()