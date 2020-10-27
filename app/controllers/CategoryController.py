from flask import render_template, redirect, flash, url_for
from app.db import session
from app.models.category import Category
from app.forms import CategoryForm

""" Controller for all category functions"""
def categories():
    form = CategoryForm()
    categories = Category.query.all()
    
    return render_template('categories.html', form = form, categories = categories, title = 'Add a Category')

def createCategory():
    form = CategoryForm()
    
    if form.validate_on_submit():
        existing_cat = Category.query.filter_by(name = form.name.data).first()
        
        if existing_cat is None:
            category = Category(
                name = form.name.data,
                description = form.description.data,
                parent_id = form.parent.data
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
            Category.parent_id: form.parent.data
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