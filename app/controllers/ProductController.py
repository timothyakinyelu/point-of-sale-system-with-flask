from flask import render_template, redirect, flash, url_for, request, make_response, jsonify
from flask_login import current_user
from sqlalchemy import or_
from app.models.product import Product
from app.models.category import Category
from app.models.brand import Brand
from app.models.pivots import category_product_table
from app.models.received import Received
from app.db import session
from app.forms import ProductForm
import logging
import logging.config
from os import path


log_file_path = path.abspath('logging.conf')
logging.config.fileConfig(log_file_path, disable_existing_loggers=False)
logger = logging.getLogger(__name__)

def products():
    """ show products template page"""
    
    return render_template('products.html')

def ajaxFetchProducts():
    """ Fetch all products from db"""
    term = request.args.get('query')
    page = request.args.get('page', 1, type=int)
    
    if term:
        products = Product.query.filter(
            or_(
                Product.name.ilike('%' + term + '%'),
                Product.sku.ilike('%' + term + '%')
            )
        ).paginate(page, 20, True)
    else:
        products = Product.query.paginate(page, 20, True)

    next_url = url_for('auth.fetchProducts', page = products.next_num) \
        if products.has_next else None
        
    prev_url = url_for('auth.fetchProducts', page = products.prev_num) \
        if products.has_prev else None

    return jsonify(results = [i.serialize for i in products.items], next_url = next_url, prev_url = prev_url, current_page = products.page, limit = products.per_page, total = products.total)

def createProduct():
    """ Add new product to the db"""
    
    records = Category.query.all()
    form = ProductForm()
    
    if form.validate_on_submit():
        existing_product = Product.query.filter_by(name = form.name.data).first()
        
        if existing_product is None:
            category = Category.query.filter(Category.id.in_(form.categories.data)).all()
            
            product = Product(
                name = form.name.data,
                sku = form.sku.data,
                gtin = form.gtin.data,
                brand_id = form.brand.data,
                price = form.price.data,
                old_price = form.old_price.data,
                discount_id = None if form.discount.data == '' else form.discount.data,
                has_discount_applied = form.apply_discount.data,
                cost_of_purchase = form.cost_of_purchase.data,
                stock_qty = form.stock_qty.data,
                min_stock_qty = form.min_stock_qty.data
            )
            product.categories.extend(category)
            session.add(product)
            session.commit()
            
            flash('Product added Successfully!')
            return redirect(url_for('auth.getProducts'))
        
        flash('Product already exists!')
        return redirect(url_for('auth.addProduct'))
    
    return render_template(
        'create_product.html', 
        form = form, 
        data_type='New Product', 
        form_action="url_for('auth.updateProduct')", 
        action = 'Add',
        categoryNames = [i.name for i in records],
        categoryIDs = [i.id for i in records]
    )

def updateProduct(product_id):
    """ Update existing product in db"""
    
    product = Product.query.filter_by(id = product_id).first()
    records = Category.query.all()
    form = ProductForm()
    
    if request.method == 'POST':
        if form.validate_on_submit():
            selected = []
            unselected = []
            
            categories = Category.query.filter(Category.id.in_(form.categories.data)).all()
            
            prod = session.query(Product).filter(Product.id == product_id).update({
                Product.name: form.name.data,
                Product.sku: form.sku.data,
                Product.brand_id: form.brand.data,
                Product.price: form.price.data,
                Product.cost_of_purchase: form.cost_of_purchase.data,
                Product.stock_qty: form.stock_qty.data,
                Product.min_stock_qty: form.min_stock_qty.data
            })
            
            link = session.query(Category).filter(Category.products.any(Product.id == product_id)).all()
            
            for x in categories:
                if x not in link:
                    selected.append(x)
            
            
            for x in link:
                if x not in categories:
                    unselected.append(x)
            
            product = Product.query.filter_by(id = product_id).first() 
            
            if unselected is not None:
                for item in unselected:
                    product.categories.remove(item)

            product.categories.extend(selected)
            session.add(product)
            session.commit()
            
            flash('Product updated Successfully!')
            return redirect(url_for('auth.getProducts'))
        
        flash('Unable to update product!')
    return render_template(
        'create_product.html', 
        form = form, 
        data_type = product.name, 
        product = product,
        form_action="/inventory/products/update-product/{}".format(product.id),
        action = 'Edit',
        categoryNames = [i.name for i in records],
        categoryIDs = [i.id for i in records]
    )

def removeProduct(id):
    """ Delete existing product"""
    
    Product.query.filter_by(id = id).delete()
    
    flash('Product deleted Successfully!')
    return redirect(url_for('auth.getProducts'))


def searchBrands():
    term = request.args.get('query')

    records = Brand.query.filter(Brand.name.ilike('%' + term + '%')).all()
    
    return jsonify(results = [i.serialize for i in records])


def getProduct():
    id = request.args.get('id')
    product = Product.query.filter_by(id = id).first()
    
    return jsonify(result = product.serialize)

def receiving():
    """ Display receiving template."""
    
    return render_template('receiving.html')

def submit_received():
    if request.method == 'POST':
        products = request.json['productID']
        product_qtys = request.json['quantity']
        cost_price = request.json['costPrice']
        selling_price = request.json['newPrice']
        supplier_id = request.json['supplierID']
        invoice_number = request.json['invoiceNumber']
        
        for i, product in enumerate(products):
            received = Received(
                product_id = int(product),
                supplier_id = int(supplier_id),
                qty_received = int(product_qtys[i]),
                cost_price = float(cost_price[i]),
                selling_price = float(selling_price[i]),
                invoice_number = invoice_number
            )
            
            session.add(received)
            session.flush()
        
        session.commit()
        data = {'message': 'Item successfully added', 'status': 201}
        logger.info(current_user.username + ' ' + 'successfully submitted item')
        return make_response(jsonify(data), 201)
    
    data = {'message': 'Unable to submit item', 'status': 400}
    logger.warn(current_user.username + ' ' + 'failed item entry')
    return make_response(jsonify(data), 400)