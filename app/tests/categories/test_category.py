from flask import url_for
from app.tests.base import BaseCase
from app.db import session
from app.models.category import Category
from app.forms import CategoryForm


class CategoryTests(BaseCase):
    def createCategory(self):
        category = Category(
            name = 'Soap',
            description = 'Soap section'
        )
        session.add(category)
        session.commit()
        
        return category

        
    def test_category_can_be_created(self):
        user = self.createUser()
        login = self.loginUser()
        
        with self.client:
            self.client.post(url_for('nonAuth.login'), data = login.data)
            response = self.client.post(url_for('auth.addCategory'), 
                data = dict(
                    name = 'Groceries',
                    description = 'Food line',
                ), 
                follow_redirects=True
            )
            
            cats = Category.query.all()

            self.assertEqual(cats[0].name, 'Groceries')
            self.assertEqual(cats[0].slug, 'groceries')
            self.assertEqual(cats[0].identifier_code, 'gr')
            
            assert b'Category created Successfully!' in response.data
            
    def test_subcategory_can_be_created(self):
        user = self.createUser()
        login = self.loginUser()
        
        existing_cat = self.createCategory()
        
        with self.client:
            self.client.post(url_for('nonAuth.login'), data = login.data)
            response = self.client.post(url_for('auth.addCategory'), 
                data = dict(
                    name = 'Hand Soap',
                    description = 'Hand soap section',
                    parent = existing_cat.id
                ), 
                follow_redirects=True
            )
            
            cats = Category.query.all()

            self.assertEqual(cats[1].name, 'Hand Soap')
            self.assertEqual(cats[1].slug, 'hand-soap')
            self.assertEqual(cats[1].identifier_code, 'ha')
            
            assert b'Category created Successfully!' in response.data
            
    def test_category_can_be_updated(self):
        user = self.createUser()
        login = self.loginUser()
        
        existing_cat = self.createCategory()
        
        with self.client:
            self.client.post(url_for('nonAuth.login'), data = login.data)
            response = self.client.post(url_for('auth.updateCategory', id = 1), 
                data = dict(
                    name = 'Soap 1',
                ), 
                follow_redirects=True
            )
            
            cats = Category.query.all()

            self.assertEqual(cats[0].name, 'Soap 1')
            
            assert b'Category updated Successfully!' in response.data
            
    def test_category_can_be_deleted(self):
        user = self.createUser()
        login = self.loginUser()
        
        existing_cat = self.createCategory()
        
        with self.client:
            self.client.post(url_for('nonAuth.login'), data = login.data)
            response = self.client.post(url_for('auth.deleteCategory', id = 1), follow_redirects=True)
            
            categories = Category.query.all()

            self.assertTrue(categories == [])
            assert b'Category deleted Successfully!' in response.data