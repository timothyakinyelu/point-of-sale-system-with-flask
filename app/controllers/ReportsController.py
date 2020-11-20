from flask import render_template, request, jsonify
from datetime import datetime, timedelta, date
from sqlalchemy import extract, func, Date
from app.models.transaction import Transaction
from app.models.product import Product
from app.db import session
import calendar


def reportsPage():
    return render_template('sales_report.html')

def allSalesByCurrentYear():
    today = datetime.today()
    current_year = today.year
    last_year = current_year - 1
    selected_year = today.year
    
    term = request.args.get('query')
    page = request.args.get('page', 1, type=int)
    search_day = extract('day', Transaction.date_created.cast(Date))
    
    if term == 'LAST_MONTH':
        month = today.month - 1 if today.month > 1 else 12
        num_days = calendar.monthrange(current_year, month)[1]
        
        start_date = date(current_year, month, 1)
        end_date = date(current_year, month, num_days)
    elif term == 'THIS_MONTH':
        month = today.month
        num_days = calendar.monthrange(current_year, month)[1]
        
        start_date = date(current_year, month, 1)
        end_date = date(current_year, month, num_days)
    elif term == 'LAST_YEAR':
        start_date = date(last_year, 1, 1)
        end_date = date(current_year, 1, 1)
    elif term is None or term == 'THIS_YEAR':
        start_date = date(current_year, 1, 1)
        end_date = date(current_year, 12, 31)
    else:
        day_period = today - timedelta(days=int(term))

        start_date = day_period
        end_date = today
    
    sales = Transaction.query.filter(Transaction.date_created.between(start_date, end_date)).\
        order_by(search_day.asc()).\
        group_by(search_day, Transaction.id).paginate(page, 20, True)
        
    next_url = url_for('auth.fetchSalesReport', page = sales.next_num) \
        if sales.has_next else None
        
    prev_url = url_for('auth.fetchSalesReport', page = sales.prev_num) \
        if sales.has_prev else None
        
    return jsonify(results = [i.serialize for i in sales.items], next_url = next_url, prev_url = prev_url, current_page = sales.page, limit = sales.per_page, total = sales.total)