from flask import render_template, redirect, flash, url_for, request
from app.db import session
from app.models.transaction import Transaction
from app.models.productTransaction import ProductTransaction


def transactions():
    transactions = Transaction.query.all()
    
    return render_template('transactions.html', transactions = transactions)
    
def new_transaction(userID, shopID):
    if request.method == 'POST':
        products = request.form.getlist('item_id')
        product_qtys = request.form.getlist('quantity')
        
        transaction = Transaction(
            user_id = userID,
            shop_id = shopID
        )
        session.add(transaction)
        session.flush()
        
        for i, product in enumerate(products):
            sales = ProductTransaction(
                product_id = int(product),
                transaction_id = transaction.id,
                product_qty = int(product_qtys[i])
            )
            
            session.add(sales)
            session.flush()
        
        session.commit()
        flash('Sale submitted Successfully!')
        return redirect(url_for('auth.addTransaction', userID = userID, shopID = shopID))
    
    return render_template('new_transaction.html', title = 'Enter new sale')
            