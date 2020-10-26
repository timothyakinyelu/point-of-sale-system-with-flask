from flask import url_for
from app.tests.base import BaseCase
from app.db import db
from app.models.brand import Brand
from app.forms import BrandForm


class BrandTests(BaseCase):
    def createBrand(self):
        brand = Brand(name = 'Apple')
        db.session.add(brand)
        db.session.commit()
        
        return brand
    
    def test_brand_can_be_created(self):
        user = self.createUser()
        login = self.loginUser()
        
        brandForm = BrandForm(name = 'Apple')
        
        with self.client:
            self.client.post(url_for('nonAuth.login'), data = login.data)
            response = self.client.post(url_for('auth.createBrand'), data = brandForm.data, follow_redirects=True)
            
            brands = Brand.query.all()

            self.assertEqual(brands[0].name, 'Apple')
            self.assertEqual(brands[0].slug, 'apple')
            self.assertEqual(brands[0].identifier_code, 'ap')
            assert b'Brand created Successfully!' in response.data
            
    
    def test_brand_already_exists(self):
        user = self.createUser()
        login = self.loginUser()
        
        existing_brand = self.createBrand()
        brandForm = BrandForm(name = 'Apple')
        
        with self.client:
            self.client.post(url_for('nonAuth.login'), data = login.data)
            response = self.client.post(url_for('auth.createBrand'), data = brandForm.data, follow_redirects=True)

            assert b'Brand name already exists!' in response.data
            
            
    def test_brand_can_be_updated(self):
        user = self.createUser()
        login = self.loginUser()
        
        existing_brand = self.createBrand()
        brandForm = BrandForm(name = 'Apple 2')
        
        with self.client:
            self.client.post(url_for('nonAuth.login'), data = login.data)
            response = self.client.post(url_for('auth.updateBrand', id = 1), data = brandForm.data, follow_redirects=True)
            
            brands = Brand.query.all()

            self.assertEqual(brands[0].name, 'Apple 2')
            assert b'Brand name updated Successfully!' in response.data
            
    def test_brand_can_be_deleted(self):
        user = self.createUser()
        login = self.loginUser()
        
        existing_brand = self.createBrand()
        
        with self.client:
            self.client.post(url_for('nonAuth.login'), data = login.data)
            response = self.client.post(url_for('auth.deleteBrand', id = 1), follow_redirects=True)
            
            brands = Brand.query.all()

            self.assertTrue(brands == [])
            assert b'Brand deleted Successfully!' in response.data