from flask import render_template, redirect, flash, url_for, request, make_response, jsonify
from app.db import session
from app.models.transaction import Transaction
from app.models.productTransaction import ProductTransaction


def transactions():
    transactions = Transaction.query.all()
    
    return render_template('transactions.html', transactions = transactions)

def new_transaction():
    return render_template('new_transaction.html', title = 'Enter new sale')
    
def submit_transaction():
    if request.method == 'POST':
        products = request.json['productID']
        product_qtys = request.json['quantity']
        
        transaction = Transaction(
            user_id = request.json['userID'],
            shop_id = request.json['shopID'],
            amount = request.json['amount'],
            payment_method = request.json['payMethod'],
            pos_ref_number = None if request.json['posRef'] == '' else request.json['posRef'],
            cost = request.json['cost']
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
        data = {'message': 'Transaction submitted Successfully', 'status': 201}
        return make_response(jsonify(data), 201)
    
    data = {'message': 'Unable to submit transaction', 'status': 400}
    return make_response(jsonify(data), 400)
            