from flask import render_template, redirect, flash, url_for, request, jsonify
from sqlalchemy import or_
from app.models.product import Product
from app.models.category import Category
from app.models.brand import Brand
from app.models.pivots import category_product_table
from app.db import session
from app.forms import ProductForm


def products():
    """ show products template page"""
    
    return render_template('products.html')

def ajaxFetchProducts():
    """ Fetch all products from db"""
    page = request.args.get('page', 1, type=int)
    
    products = Product.query.paginate(page, 2, True)
    next_url = url_for('auth.fetchProducts', page = products.next_num) \
        if products.has_next else None
        
    prev_url = url_for('auth.fetchProducts', page = products.prev_num) \
        if products.has_prev else None

    return jsonify(products = [i.serialize for i in products.items], next_url = next_url, prev_url = prev_url, current_page = products.page, limit = products.per_page, total = products.total)

def createProduct():
    """ Add new product to the db"""
    
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
    
    return render_template('create_product.html', form = form, title = 'Add Product')

def updateProduct(id):
    """ Update existing product in db"""
    
    form = ProductForm()
    
    if form.validate_on_submit():
        selected = []
        unselected = []
        
        categories = Category.query.filter(Category.id.in_(form.categories.data)).all()
        
        prod = session.query(Product).filter(Product.id == id).update({
            Product.name: form.name.data,
            Product.sku: form.sku.data,
            Product.brand_id: form.brand.data,
            Product.price: form.price.data,
            Product.cost_of_purchase: form.cost_of_purchase.data,
            Product.stock_qty: form.stock_qty.data,
            Product.min_stock_qty: form.min_stock_qty.data
        })
        
        link = session.query(Category).filter(Category.products.any(Product.id == prod)).all()
        
        for x in categories:
            if x not in link:
                selected.append(x)
        
        
        for x in link:
            if x not in categories:
                unselected.append(x)
        
        product = Product.query.filter_by(id = prod).first() 
        
        if unselected is not None:
            for item in unselected:
                product.categories.remove(item)

        product.categories.extend(selected)
        
        flash('Product updated Successfully!')
        return redirect(url_for('auth.getProducts'))
    
    flash('Unable to update product!')
    return render_template('create_product.html', form = form, title = 'Update Product')

def removeProduct(id):
    """ Delete existing product"""
    
    Product.query.filter_by(id = id).delete()
    
    flash('Product deleted Successfully!')
    return redirect(url_for('auth.getProducts'))


def searchBrands():
    term = request.args.get('query')

    records = Brand.query.filter(Brand.name.ilike('%' + term + '%')).all()
    
    return jsonify(results = [i.serialize for i in records])


def searchProducts():
    term = request.args.get('query')

    records = Product.query.filter(
        or_(
            Product.name.ilike('%' + term + '%'),
            Product.sku.ilike('%' + term + '%')
        )
    ).all()
    
    return jsonify([i.serialize for i in records])


def getProduct():
    id = request.args.get('id')
    product = Product.query.filter_by(id = id).first()
    
    return jsonify(result = product.serialize)