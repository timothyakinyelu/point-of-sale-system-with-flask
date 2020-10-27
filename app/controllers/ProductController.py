from flask import render_template, redirect, flash, url_for
from app.models.product import Product
from app.models.category import Category
from app.models.pivots import category_product_table
from app.db import session
from app.forms import ProductForm


def products():
    products = Product.query.all()
    
    return render_template('products.html', products = products)

def createProduct():
    form = ProductForm()
    
    if form.validate_on_submit():
        existing_product = Product.query.filter_by(name = form.name.data).first()
        
        if existing_product is None:
            category = Category.query.filter(Category.id.in_(form.categories.data)).all()
            
            product = Product(
                name = form.name.data,
                sku = form.sku.data,
                brand_id = form.brand.data,
                price = form.price.data,
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
    
    flash('Unable to add product!')
    return render_template('create_product.html', form = form, title = 'Add Product')

def updateProducts(id):
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