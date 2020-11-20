from flask import render_template, request, jsonify, current_app
from datetime import datetime, timedelta
from sqlalchemy import extract, func, Date
from app.models.transaction import Transaction
from app.models.product import Product
from app.db import session
import calendar

def get_count(q):
    count_q = q.statement.with_only_columns([func.count()]).order_by(None)
    count = q.session.execute(count_q).scalar()
    return count

def dashboard():
    """ Display year sales and cost of products sold."""
    
    today = datetime.today()
    selected_year = today.year
    
    search_year = extract('year', Transaction.date_created)
    
    orders = Transaction.query.with_entities(func.sum(Transaction.amount).label("total_amount")).filter(search_year == selected_year).first()
    
    purchases = Transaction.query.with_entities(func.sum(Transaction.cost).label("total_cost")).filter(search_year == selected_year).first()
    
    products = Product.query.filter(Product.stock_qty == Product.min_stock_qty)
    item_count = get_count(products)
    
    sales = "{}{:,.2f}".format(current_app.config['CURRENCY_ICON'], float(orders.total_amount)) \
        if orders.total_amount else 0.00
        
    costs = "{}{:,.2f}".format(current_app.config['CURRENCY_ICON'], float(purchases.total_cost)) \
        if purchases.total_cost else 0.00
    
    return render_template(
        'dashboard.html', 
        sales = sales, 
        costs = costs,
        product_count = item_count
    )

def chart():
    """ Fetch chart data from db using period information."""
    
    today = datetime.today()
    selected_week = today.weekday()
    mon = today - timedelta(days=selected_week)
    sun = today + timedelta(days=(6 - selected_week))
    
    period = request.args.get('period')
    filter_value = extract(period, Transaction.date_created.cast(Date))
    search_day = extract('day', Transaction.date_created.cast(Date))
    day_of_week = extract('dow', Transaction.date_created.cast(Date))
    
    if period == 'month':
        sales = Transaction.query.with_entities(func.sum(Transaction.amount).label("total_amount"), filter_value).\
            order_by(filter_value.asc()).\
            group_by(filter_value).limit(12).all()
            
        periods = Transaction.query.with_entities(filter_value.label(period)).\
            order_by(filter_value.asc()).\
            group_by(filter_value).limit(12).all()
            
        labels = [calendar.month_name[int(i)] for sub in periods for i in sub]
    else:
        sales = Transaction.query.with_entities(func.sum(Transaction.amount).label("total_amount"), search_day).\
                filter(Transaction.date_created.between(mon, sun)).\
                order_by(search_day.asc()).\
                group_by(search_day).limit(7).all()
        
        periods = Transaction.query.with_entities(day_of_week.label(period)).\
                filter(Transaction.date_created.between(mon, sun)).\
                order_by(search_day.asc()).\
                group_by(search_day, day_of_week).limit(7).all()
    
        labels = [calendar.day_name[int(i)-1] for sub in periods for i in sub]
    
    legend = 'Sales Data'
    values = sales
    return jsonify(labels = labels, legend = legend, values = values)