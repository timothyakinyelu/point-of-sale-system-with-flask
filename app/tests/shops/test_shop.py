from flask import url_for
from app.tests.base import BaseCase
from app.db import db
from app.models.shop import Shop
from app.forms import ShopForm


class ShopTests(BaseCase):
    def test_shop_can_be_created(self):
        user = self.createUser()
        login = self.loginUser()
        
        shopForm = ShopForm(name = 'SuperMarket')
        
        with self.client:
            self.client.post(url_for('nonAuth.login'), data = login.data)
            response = self.client.post(url_for('auth.createShop'), data = shopForm.data, follow_redirects=True)
            
            shops = Shop.query.all()

            self.assertEqual(shops[0].name, 'SuperMarket')
            self.assertEqual(shops[0].slug, 'supermarket')
            assert b'Shop created Successfully!' in response.data
            
    
    def test_shop_already_exists(self):
        user = self.createUser()
        login = self.loginUser()
        
        existing_shop = Shop(name = 'SuperMarket')
        db.session.add(existing_shop)
        db.session.commit()
        
        shopForm = ShopForm(name = 'SuperMarket')
        
        with self.client:
            self.client.post(url_for('nonAuth.login'), data = login.data)
            response = self.client.post(url_for('auth.createShop'), data = shopForm.data, follow_redirects=True)

            assert b'Shop name already exists!' in response.data
            
            
    def test_shop_can_be_updated(self):
        user = self.createUser()
        login = self.loginUser()
        
        existing_shop = Shop(name = 'SuperMarket')
        db.session.add(existing_shop)
        db.session.commit()
        
        shopForm = ShopForm(name = 'Mini-Mart')
        
        with self.client:
            self.client.post(url_for('nonAuth.login'), data = login.data)
            response = self.client.post(url_for('auth.updateShop', id = 1), data = shopForm.data, follow_redirects=True)
            
            shops = Shop.query.all()

            self.assertEqual(shops[0].name, 'Mini-Mart')
            assert b'Shop name updated Successfully!' in response.data
            
    def test_shop_can_be_deleted(self):
        user = self.createUser()
        login = self.loginUser()
        
        existing_shop = Shop(name = 'SuperMarket')
        db.session.add(existing_shop)
        db.session.commit()
        
        with self.client:
            self.client.post(url_for('nonAuth.login'), data = login.data)
            response = self.client.post(url_for('auth.deleteShop', id = 1), follow_redirects=True)
            
            shops = Shop.query.all()

            self.assertTrue(shops == [])
            assert b'Shop deleted Successfully!' in response.data