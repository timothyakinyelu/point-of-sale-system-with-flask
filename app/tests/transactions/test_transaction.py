from flask import url_for
from app.tests.base import BaseCase
from app.models.transaction import Transaction
from app.models.productTransaction import ProductTransaction
from app.models.shop import Shop
from app.models.product import Product
from app.db import session
from app.forms import TransactionForm
from flask_login import current_user


class TransactionTests(BaseCase):
    def test_transactions_can_be_completed(self):
        user = self.createUser()
        login = self.loginUser()
        
        shop = Shop(name = 'SuperMarket')
        session.add(shop)
        session.commit()
        
        prod1 = Product(
            name = 'Dettol cool 200mg',
            brand_id = 1,
            sku = 'so-de-co-200',
            price = 300.00,
            stock_qty = 50
        )
        prod2 = Product(
            name = 'Dettol cool 100mg',
            brand_id = 1,
            sku = 'so-de-co-100',
            price = 250.00,
            stock_qty = 30
        )
        session.add(prod1)
        session.add(prod2)
        session.commit()

                
        with self.client:
            self.client.post(url_for('nonAuth.login'), data = login.data)
            response = self.client.post(url_for('auth.addTransaction', userID = current_user.id, shopID = shop.id), 
                data = dict(
                    item_id = [prod1.id, prod2.id],
                    quantity = [20, 25]
                ),
                follow_redirects = True
            )

            transactions = session.query(ProductTransaction).all()
            products = Product.query.all()
            
            self.assertEqual(transactions[0].product_qty, 20)
            self.assertEqual(transactions[1].product_qty, 25)
            self.assertEqual(products[0].stock_qty, 30)
            self.assertEqual(products[1].stock_qty, 5)
            
            assert b'Sale submitted Successfully!' in response.data