from flask import render_template, redirect, url_for, flash, request, jsonify
from app.models.brand import Brand
from app.db import session
from app.forms import BrandForm

""" Controller for all brand functions"""
def brands():
    """ get all brands from db"""
    form = BrandForm()
    
    return render_template('brands.html',form = form, title = 'Add a Brand')

def ajaxFetchBrands():
    """ Fetch all brands from db"""
    term = request.args.get('query')
    page = request.args.get('page', 1, type=int)
    
    if term:
        brands = Brand.query.filter(
            Brand.name.ilike('%' + term + '%')
        ).paginate(page, 20, True)
    else:
        brands = Brand.query.paginate(page, 20, True)

    next_url = url_for('auth.fetchBrands', page = brands.next_num) \
        if brands.has_next else None
        
    prev_url = url_for('auth.fetchBrands', page = brands.prev_num) \
        if brands.has_prev else None

    return jsonify(results = [i.serialize for i in brands.items], next_url = next_url, prev_url = prev_url, current_page = brands.page, limit = brands.per_page, total = brands.total)


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
