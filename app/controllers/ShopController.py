from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import current_user
from app.models.shop import Shop
from app.db import session
from app.forms import ShopForm
import logging
import logging.config
from os import path


log_file_path = path.abspath('logging.conf')
logging.config.fileConfig(log_file_path, disable_existing_loggers=False)
logger = logging.getLogger(__name__)

""" Controller for all shop functions"""
def shops():
    """ get all shops from db"""
    
    return render_template('shops.html')

def ajaxFetchShops():
    """ Fetch all users from db"""
    term = request.args.get('query')
    page = request.args.get('page', 1, type=int)
    
    if term:
        shops = Shop.query.filter(
            Shop.name.ilike('%' + term + '%'),     
        ).paginate(page, 20, True)
    else:
        shops = Shop.query.paginate(page, 20, True)

    next_url = url_for('auth.fetchShops', page = shops.next_num) \
        if shops.has_next else None
        
    prev_url = url_for('auth.fetchShops', page = shops.prev_num) \
        if shops.has_prev else None

    return jsonify(results = [i.serialize for i in shops.items], next_url = next_url, prev_url = prev_url, current_page = shops.page, limit = shops.per_page, total = shops.total)

def createShop():
    """ create a new shop"""
    form = ShopForm()
    
    if request.method == 'POST':
        if not form.name.data[0].isdigit():
            if form.validate_on_submit():
                exising_shop = Shop.query.filter_by(name = form.name.data).first()
                
                if exising_shop is None:
                    shop = Shop(
                        name = form.name.data
                    )
                    session.add(shop)
                    session.commit()
                    
                    flash('Shop created Successfully!')
                    return redirect(url_for('auth.getShops'))

                flash('Shop name already exists!')
        flash('Shop name must start with a letter')
    
    return render_template(
        'create_role.html', 
        form = form, 
        data_type='New Shop', 
        form_action=url_for('auth.addShop'), 
        action = 'Add',
    )
                

def updateShop(shop_id):
    """ update existing shop in db"""
    
    form = ShopForm()
    if request.method == 'GET':
        shop = Shop.query.filter_by(id = shop_id).first()
        form.name.data = shop.name
        
    if request.method == 'POST':
        if not form.name.data[0].isdigit():
            if form.validate_on_submit():
                session.query(Shop).filter(Shop.id == shop_id).update({Shop.name: form.name.data})
                
                session.commit()
                flash('Shop name updated Successfully!')
                return redirect(url_for('auth.getShops'))

            flash('Unable to update shop name!')
        flash('Value entered must start with an alphabet!')
    
    return render_template(
        'create_shop.html',
        form = form, 
        data_type = shop.name,
        form_action=url_for('auth.updateShop', shop_id = shop.id),
        action = 'Edit',
    )


def removeShop():
    """ delete shops form db"""
    
    if request.method == 'POST':
        ids = request.json['selectedIDs']
        
        session.query(Shop).filter(Shop.id.in_(ids)).delete(synchronize_session=False)
        session.commit()
        
        data = {'message': 'Shop(s) deleted Successfully!', 'status': 200}
        logger.warn(current_user.username + ' ' + 'deleted shop(s)')
        return make_response(jsonify(data), 200)