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
    
    start = request.args.get('start')
    end = request.args.get('end')

    page = request.args.get('page', 1, type=int)
    search_day = extract('day', Transaction.date_created.cast(Date))
    
    if start is None and end is None:
        start_date = date(current_year, 1, 1)
        end_date = date(current_year, 12, 31) 
    else:
        start_date = date.fromisoformat(start)     
        end_date = date.fromisoformat(end)     
    
    sales = Transaction.query.filter(Transaction.date_created.between(start_date, end_date)).\
        order_by(search_day.asc()).\
        group_by(search_day, Transaction.id).paginate(page, 20, True)
        
    next_url = url_for('auth.fetchSalesReport', page = sales.next_num) \
        if sales.has_next else None
        
    prev_url = url_for('auth.fetchSalesReport', page = sales.prev_num) \
        if sales.has_prev else None
        
    return jsonify(results = [i.serialize for i in sales.items], next_url = next_url, prev_url = prev_url, current_page = sales.page, limit = sales.per_page, total = sales.total)