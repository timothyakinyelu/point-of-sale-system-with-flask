from flask import render_template, redirect, url_for, flash
from app.models.brand import Brand
from app.db import session
from app.forms import BrandForm

""" Controller for all brand functions"""
def brands():
    """ get all brands from db"""
    form = BrandForm()
    brands = Brand.query.all()
    
    return render_template('brands.html', brands = brands, form = form, title = 'Add a Brand')

def createBrand():
    """ create a new brand"""
    form = BrandForm()
    
    if not form.name.data[0].isdigit():
        if form.validate_on_submit():
            exising_brand = Brand.query.filter_by(name = form.name.data).first()
            
            if exising_brand is None:
                brand = Brand(
                    name = form.name.data
                )
                session.add(brand)
                session.commit()
                
                flash('Brand created Successfully!')
                return redirect(url_for('auth.getBrands'))

            flash('Brand name already exists!')
    flash('Brand name must start with a letter')
    
    return redirect(url_for('auth.getBrands'))
                

def updateBrand(id):
    """ update existing brand in db"""
    form = BrandForm()
    
    if not form.name.data[0].isdigit():
        if form.validate_on_submit():
            session.query(Brand).filter(Brand.id == id).update({Brand.name: form.name.data})
            
            flash('Brand name updated Successfully!')
            return redirect(url_for('auth.getBrands'))

        flash('Unable to update brand name!')
    flash('Value entered must start with an alphabet!')
    
    return redirect(url_for('auth.getBrands'))


def removeBrand(id):
    """ delete brand from db"""
    Brand.query.filter_by(id = id).delete()
    flash('Brand deleted Successfully!')
    
    return redirect(url_for('auth.getBrands'))