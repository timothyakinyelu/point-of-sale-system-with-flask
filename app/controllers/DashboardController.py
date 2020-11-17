from flask import render_template, json
from datetime import datetime
from sqlalchemy import extract, func
from app.models.transaction import Transaction
from app.db import session

def dashboard():
    today = datetime.today()
    selected_year = today.year
    
    search_year = extract('year', Transaction.date_created)
    orders = Transaction.query.with_entities(func.sum(Transaction.amount).label("total_amount")).filter(search_year == selected_year).first()
    
    purchases = Transaction.query.with_entities(func.sum(Transaction.cost).label("total_cost")).filter(search_year == selected_year).first()
    
    sales = "₦{:,.2f}".format(float(orders.total_amount)) \
        if orders.total_amount else 0.00
        
    costs = "₦{:,.2f}".format(float(purchases.total_cost)) \
        if purchases.total_cost else 0.00
    
    legend = json.dumps('Monthly Data')
    labels = json.dumps(["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"])
    values = json.dumps([10, 9, 8, 7, 6, 4, 7, 8, 5, 8, 3, 7])
    
    return render_template(
        'dashboard.html', 
        labels = labels, 
        legend = legend, 
        values = values, 
        sales = sales, 
        costs = costs
    )

# def chart():
#     legend = 'Monthly Data'
#     labels = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
#     values = [10, 9, 8, 7, 6, 4, 7, 8, 5, 8, 3, 7]
#     return jsonify(labels = labels, legend = legend, values = values)