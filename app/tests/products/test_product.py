from flask import url_for
from app.tests.base import BaseCase
from app.models.product import Product
from app.models.category import Category
from app.models.brand import Brand
from app.models.pivots import category_product_table
from app.db import session
from app.forms import ProductForm

class ProductTests(BaseCase):
    def test_product_can_be_created(self):
        user = self.createUser()
        login = self.loginUser()
        
        brand = Brand(name = 'Apple')
        category = Category(name = 'Soap')
        session.add(brand)
        session.add(category)
        session.commit()
        
        with self.client:
            self.client.post(url_for('nonAuth.login'), data = login.data)
            response = self.client.post(url_for('auth.addProduct'), 
                data = dict(
                    name = 'Sparkling Hand Wash 200ml',
                    sku = 'ap-so-shw-200',
                    brand = brand.id,
                    categories = category.id,
                    price = 300.00,
                    cost_of_purchase = 250.00,
                    stock_qty = 20,
                    min_stock_qty = 5
                ),
                follow_redirects = True
            )
            
            products = Product.query.all()
            link = session.query(category_product_table).all()
            
            self.assertEqual(products[0].name, 'Sparkling Hand Wash 200ml')
            self.assertEqual(products[0].sku, 'ap-so-shw-200')
            self.assertEqual(products[0].price, 300.00)
            self.assertEqual(link[0].category_id, category.id)
            
            assert b'Product added Successfully!' in response.data
            
    def test_product_can_be_updated(self):
        user = self.createUser()
        login = self.loginUser()
        
        brand = Brand(name = 'Apple')
        category1 = Category(name = 'Soap')
        category2 = Category(name = 'Bath')
        category3 = Category(name = 'Make Up')
        session.add(brand)
        session.add(category1)
        session.add(category2)
        session.add(category3)
        session.commit()
        
        product = Product(
            name = 'Sparkling Hand Wash 200ml',
            sku = 'ap-so-shw-200',
            brand_id = brand.id,
            price = 300.00,
            cost_of_purchase = 250.00,
            stock_qty = 20,
            min_stock_qty = 5
        )
        categories = [category1, category2]
        product.categories.extend(categories)
        session.add(product)
        session.commit()
            
        with self.client:
            self.client.post(url_for('nonAuth.login'), data = login.data)
            response = self.client.post(url_for('auth.updateProduct', id = 1), 
                data = dict(
                    name = 'Sparkling Hand Wash 200ml',
                    sku = 'ap-so-shw-200',
                    brand = brand.id,
                    categories = [category1.id, category3.id],
                    price = 300.00,
                    cost_of_purchase = 250.00,
                    stock_qty = 20,
                    min_stock_qty = 5
                ),
                follow_redirects = True
            )
            
            link = session.query(category_product_table).all()
            
            self.assertEqual(link[1].category_id, category3.id)
            
            assert b'Product updated Successfully!' in response.data
            
    def test_product_can_be_deleted(self):
        user = self.createUser()
        login = self.loginUser()
        
        product = Product(
            name = 'Sparkling Hand Wash 200ml',
            sku = 'ap-so-shw-200',
            brand_id = 1,
            price = 300.00,
            cost_of_purchase = 250.00,
            stock_qty = 20,
            min_stock_qty = 5
        )

        session.add(product)
        session.commit()
        
        with self.client:
            self.client.post(url_for('nonAuth.login'), data = login.data)
            response = self.client.post(url_for('auth.deleteProduct', id = 1), follow_redirects = True)
            
            products = Product.query.all()
            
            self.assertEqual(products, [])
            
            assert b'Product deleted Successfully!' in response.data