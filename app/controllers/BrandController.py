from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import current_user
from app.models.brand import Brand
from app.db import session
from app.forms import BrandForm
import logging
import logging.config
from os import path


log_file_path = path.abspath('logging.conf')
logging.config.fileConfig(log_file_path, disable_existing_loggers=False)
logger = logging.getLogger(__name__)

""" Controller for all brand functions"""
def brands():
    """ get all brands from db"""
    
    return render_template('brands.html')

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
    
    if request.method == 'POST':
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

    return render_template(
        'create_brand.html', 
        form = form, 
        data_type='New Brand', 
        form_action=url_for('auth.addBrand'), 
        action = 'Add',
    )
                

def updateBrand(brand_id):
    """ update existing brand in db"""
    
    form = BrandForm()
    if request.method == 'GET':
        brand = Brand.query.filter_by(id = brand_id).first()
        form.name.data = brand.name
        
    if request.method == 'POST':
        if not form.name.data[0].isdigit():
            if form.validate_on_submit():
                session.query(Brand).filter(Brand.id == brand_id).update({Brand.name: form.name.data})
                
                session.commit()
                flash('Brand name updated Successfully!')
                return redirect(url_for('auth.getBrands'))

            flash('Unable to update brand name!')
        flash('Value entered must start with an alphabet!')
    
    return render_template(
        'create_brand.html',
        form = form, 
        data_type = brand.name,
        form_action=url_for('auth.updateBrand', brand_id = brand.id),
        action = 'Edit',
    )


def removeBrand():
    if request.method == 'POST':
        ids = request.json['selectedIDs']
        
        session.query(Brand).filter(Brand.id.in_(ids)).delete(synchronize_session=False)
        session.commit()
        
        data = {'message': 'Brand(s) deleted Successfully!', 'status': 200}
        logger.warn(current_user.username + ' ' + 'deleted brand(s)')
        return make_response(jsonify(data), 200)
