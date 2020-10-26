from flask import render_template, redirect, url_for, flash
from app.models.shop import Shop
from app.db import session
from app.forms import ShopForm

""" Controller for all shop functions"""
def shops():
    """ get all shops from db"""
    form = ShopForm()
    shops = Shop.query.all()
    
    return render_template('shops.html', shops = shops, form = form, title = 'Create a Shop')

def createShops():
    """ create a new shop"""
    form = ShopForm()
    
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
    
    return redirect(url_for('auth.getShops'))
                

def updateShops(id):
    """ update existing shop in db"""
    form = ShopForm()
    
    if not form.name.data[0].isdigit():
        if form.validate_on_submit():
            session.query(Shop).filter(Shop.id == id).update({Shop.name: form.name.data})
            
            flash('Shop name updated Successfully!')
            return redirect(url_for('auth.getShops'))

        flash('Unable to update shop name!')
    flash('Value entered must start with an alphabet!')
    
    return redirect(url_for('auth.getShops'))


def deleteShops(id):
    """ delete shop from db"""
    Shop.query.filter_by(id = id).delete()
    flash('Shop deleted Successfully!')
    
    return redirect(url_for('auth.getShops'))