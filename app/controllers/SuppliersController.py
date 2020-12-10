from flask import render_template, redirect, flash, url_for, request, jsonify
from app.models.supplier import Supplier
from app.db import session
from sqlalchemy import or_
from app.forms import SupplierForm
import logging
import logging.config
from os import path


log_file_path = path.abspath('logging.conf')
logging.config.fileConfig(log_file_path, disable_existing_loggers=False)
logger = logging.getLogger(__name__)

def suppliers():
    """ show suppliers template page"""
    
    return render_template('suppliers.html')

def ajaxFetchSuppliers():
    """ Fetch all suppliers from db"""
    term = request.args.get('query')
    page = request.args.get('page', 1, type=int)
    
    if term:
        suppliers = Supplier.query.filter(
            or_(
                Supplier.name.ilike('%' + term + '%'),
                Supplier.account_number.ilike('%' + term + '%'),
                Supplier.state.ilike('%' + term + '%'),
                Supplier.phone_number.ilike('%' + term + '%')
            )
        ).paginate(page, 20, True)
    else:
        suppliers = Supplier.query.paginate(page, 20, True)

    next_url = url_for('auth.fetchSuppliers', page = suppliers.next_num) \
        if suppliers.has_next else None
        
    prev_url = url_for('auth.fetchSuppliers', page = suppliers.prev_num) \
        if suppliers.has_prev else None

    return jsonify(results = [i.serialize for i in suppliers.items], next_url = next_url, prev_url = prev_url, current_page = suppliers.page, limit = suppliers.per_page, total = suppliers.total)

def createSupplier():
    """ Add new supplier to the db"""
    
    form = SupplierForm(status = 'PENDING')
    
    if form.validate_on_submit():
        existing_supplier = Supplier.query.filter_by(name = form.name.data).first()
        
        if existing_supplier is None:
            supplier = Supplier(
                name = form.name.data,
                phone_number = form.phone.data,
                email = form.email.data,
                address = form.address.data,
                state = form.state.data,
                account_number = form.account.data,
                status = form.status.data
            )
            session.add(supplier)
            session.commit()
            
            flash('Supplier added Successfully!')
            return redirect(url_for('auth.getSuppliers'))
        
        flash('Supplier already exists!')
        return redirect(url_for('auth.addSupplier'))
    
    return render_template(
        'create_supplier.html', 
        form = form, 
        data_type='New Supplier', 
        form_action=url_for('auth.addSupplier'), 
        action = 'Add',
    )

def updateSupplier(supplier_id):
    """ Update existing supplier in db"""
    supplier = Supplier.query.filter_by(id = supplier_id).first()
    form = SupplierForm(status = supplier.status)
    
    if request.method == 'POST':
        if form.validate_on_submit():
            updatedSupplier = session.query(Supplier).filter(Supplier.id == supplier_id).update({
                Supplier.name: form.name.data,
                Supplier.phone_number: form.phone.data,
                Supplier.email: form.email.data,
                Supplier.address: form.address.data,
                Supplier.state: form.state.data,
                Supplier.account_number: form.account.data,
                Supplier.status: form.status.data
            })
            
            session.commit()
            
            flash('Supplier updated Successfully!')
            return redirect(url_for('auth.getSuppliers'))
        
        flash('Unable to update supplier!')
    return render_template(
        'create_supplier.html',
        form = form, 
        data_type = supplier.name, 
        supplier = supplier,
        form_action=url_for('auth.updateSupplier', supplier_id = supplier.id),
        action = 'Edit',
    )

def removeSupplier():
    """ delete suppliers form db"""
    
    if request.method == 'POST':
        ids = request.json['selectedIDs']
        
        session.query(Supplier).filter(Supplier.id.in_(ids)).delete(synchronize_session=False)
        session.commit()
        
        data = {'message': 'Supplier(s) deleted Successfully!', 'status': 200}
        logger.warn(current_user.username + ' ' + 'deleted supplier(s)')
        return make_response(jsonify(data), 200)

def getSupplier():
    id = request.args.get('id')
    supplier = Supplier.query.filter_by(id = id).first()
    
    return jsonify(result = supplier.serialize)

