from flask import render_template, request, url_for, jsonify
from datetime import date, datetime
from sqlalchemy import extract, func, Date, or_
from app.models.transaction import Transaction
from app.models.product import Product
from app.models.user import User
from app.models.productTransaction import ProductTransaction
from app.db import session


def salesReports():
    """ Render sales report template."""
    return render_template('sales_report.html')

def allSalesReport():
    """ Fetch all sales into a report table."""
    
    term = request.args.get('query')
    start = request.args.get('start')
    end = request.args.get('end')

    page = request.args.get('page', 1, type=int)
    search_day = extract('day', Transaction.date_created.cast(Date))
    
    if term:
        sales = Transaction.query.\
        join(Transaction.user).\
        filter(
            or_(
                Transaction.payment_method.ilike('%' + term + '%'),
                Transaction.pos_ref_number.ilike('%' + term + '%'),
                User.username.ilike('%' + term + '%')
            )
        ).paginate(page, 20, True)
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


def productsReports():
    """ Render products report template."""
    return render_template('products_report.html')

def allProductsReport():
    term = request.args.get('query')
    start = request.args.get('start')
    end = request.args.get('end')

    page = request.args.get('page', 1, type=int)
    search_day = extract('day', Transaction.date_created.cast(Date))
    
    if term:
        products = ProductTransaction.query.\
            join(ProductTransaction.product).\
            join(ProductTransaction.transaction).\
            filter(
                or_(
                    Product.name.ilike('%' + term + '%'),
                )
            ).\
            order_by(search_day.asc()).paginate(page, 20, True)
    else:
        start_date = date.fromisoformat(start)     
        end_date = date.fromisoformat(end)   
    
        products = session.query(ProductTransaction).join(ProductTransaction.transaction).\
            filter(ProductTransaction.transaction_id == Transaction.id).\
            filter(Transaction.date_created.between(start_date, end_date)).\
            order_by(search_day.asc()).paginate(page, 20, True)
    
    next_url = url_for('auth.fetchProductsReport', page = products.next_num) \
        if products.has_next else None
        
    prev_url = url_for('auth.fetchProductsReport', page = products.prev_num) \
        if products.has_prev else None
        
    return jsonify(results = [i.serialize for i in products.items], next_url = next_url, prev_url = prev_url, current_page = products.page, limit = products.per_page, total = products.total)

def lowStocksReport():
    return render_template('low_stock.html')

def allLowStocks():
    term = request.args.get('query')
    page = request.args.get('page', 1, type=int)
    
    if term:
        products = Product.query.filter(Product.stock_qty == Product.min_stock_qty).\
            filter(
                or_(
                    Product.name.ilike('%' + term + '%'),
                    Product.sku.ilike('%' + term + '%')
                )
            ).\
            paginate(page, 20, True)
    else:
        products = Product.query.filter(Product.stock_qty == Product.min_stock_qty).\
            paginate(page, 20, True)
        
    next_url = url_for('auth.fetchLowStocks', page = products.next_num) \
        if products.has_next else None
        
    prev_url = url_for('auth.fetchLowStocks', page = products.prev_num) \
        if products.has_prev else None
        
    return jsonify(results = [i.serialize for i in products.items], next_url = next_url, prev_url = prev_url, current_page = products.page, limit = products.per_page, total = products.total)
    

def salesByCurrentDate():
    return render_template('today-sales.html')

def getTodaySales():
    value = datetime.today()
    now = value.strftime("%Y-%m-%d")
    page = request.args.get('page', 1, type=int)

    sales = Transaction.query.join(ProductTransaction).\
        filter(Transaction.date_created.cast(Date) == now).\
        order_by(Transaction.user_id).\
        group_by(Transaction.user_id, Transaction.id).paginate(page, 20, True)
        
    next_url = url_for('auth.fetchTodaySales', page = sales.next_num) \
        if sales.has_next else None
        
    prev_url = url_for('auth.fetchTodaySales', page = sales.prev_num) \
        if sales.has_prev else None

    return jsonify(results = [i.serialize for i in sales.items], next_url = next_url, prev_url = prev_url, current_page = sales.page, limit = sales.per_page, total = sales.total)