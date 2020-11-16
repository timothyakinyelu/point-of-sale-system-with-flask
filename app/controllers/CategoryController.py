from flask import render_template, redirect, flash, url_for, request, jsonify
from app.db import session
from app.models.category import Category
from app.forms import CategoryForm

""" Controller for all category functions"""
def categories():
    form = CategoryForm()
    # categories = Category.query.all()
    
    return render_template('categories.html', form = form, title = 'Add a Category')

def ajaxFetchCategories():
    """ Fetch all products from db"""
    term = request.args.get('query')
    page = request.args.get('page', 1, type=int)
    
    if term:
        categories = Category.query.filter(
            Category.name.ilike('%' + term + '%')
        ).order_by(Category.display_order.desc()).paginate(page, 20, True)
    else:
        categories = Category.query.order_by(Category.display_order, Category.parent_id.desc()).paginate(page, 20, True)

    next_url = url_for('auth.fetchCategories', page = categories.next_num) \
        if categories.has_next else None
        
    prev_url = url_for('auth.fetchCategories', page = categories.prev_num) \
        if categories.has_prev else None

    return jsonify(results = [i.serialize for i in categories.items], next_url = next_url, prev_url = prev_url, current_page = categories.page, limit = categories.per_page, total = categories.total)

def createCategory():
    form = CategoryForm()
    
    if form.validate_on_submit():
        existing_cat = Category.query.filter_by(name = form.name.data).first()
        
        if existing_cat is None:
            category = Category(
                name = form.name.data,
                description = form.description.data,
                parent_id = None if form.parent.data == 0 else form.parent.data
            )
            
            session.add(category)
            session.commit()
            
            flash('Category created Successfully!')
            return redirect(url_for('auth.getCategories'))
        
        flash('Category already exists!')
    flash('Unable to create Category!')
    return redirect(url_for('auth.getCategories'))

def updateCategory(id):
    form = CategoryForm()
    
    if form.validate_on_submit():
        session.query(Category).filter(Category.id == id).update({
            Category.name: form.name.data,
            Category.description: form.description.data,
            Category.parent_id: None if form.parent.data == 0 else form.parent.data
        })
        
        flash('Category updated Successfully!')
        return redirect(url_for('auth.getCategories'))
    
    flash('Unable to update category!')
    return redirect(url_for('auth.getCategories'))

def removeCategory(id):
    """ delete category from db"""
    
    Category.query.filter_by(id = id).delete()
    flash('Category deleted Successfully!')
    
    return redirect(url_for('auth.getCategories'))