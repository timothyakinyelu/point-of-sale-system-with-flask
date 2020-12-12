from flask import render_template, redirect, flash, url_for, request, jsonify
from flask_login import current_user
from app.db import session
from app.models.category import Category
from app.forms import CategoryForm
import logging
import logging.config
from os import path


log_file_path = path.abspath('logging.conf')
logging.config.fileConfig(log_file_path, disable_existing_loggers=False)
logger = logging.getLogger(__name__)

""" Controller for all category functions"""
def categories():
    """ show categories template page"""
    
    return render_template('categories.html')

def ajaxFetchCategories():
    """ Fetch all brands from db"""
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
    
    if request.method == 'POST':
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
    return render_template(
        'create_category.html', 
        form = form, 
        data_type='New Category', 
        form_action=url_for('auth.addCategory'), 
        action = 'Add',
    )

def updateCategory(category_id):
    """Update existing category in database."""
    
    form = CategoryForm()
    if request.method == 'GET':
        category = Category.query.filter_by(id = category_id).first()
        form.description.data = category.description
        form.parent.data = category.parent_id
    
    if request.method == 'POST':
        if form.validate_on_submit():
            session.query(Category).filter(Category.id == category_id).update({
                Category.name: form.name.data,
                Category.description: form.description.data,
                Category.parent_id: None if form.parent.data == 0 else form.parent.data
            })
            
            session.commit()
            
            flash('Category updated Successfully!')
            return redirect(url_for('auth.getCategories'))
        
        flash('Unable to update category!')

    return render_template(
        'create_category.html', 
        form = form, 
        data_type = category.name, 
        category = category,
        form_action=url_for('auth.updateCategory', category_id = category.id),
        action = 'Edit',
    )

def removeCategory():
    if request.method == 'POST':
        ids = request.json['selectedIDs']
        
        session.query(Category).filter(Category.id.in_(ids)).delete(synchronize_session=False)
        session.commit()
        
        data = {'message': 'Categories deleted Successfully!', 'status': 200}
        logger.warn(current_user.username + ' ' + 'deleted categories')
        return make_response(jsonify(data), 200)