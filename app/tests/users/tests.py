from flask import url_for
from app.tests.base import BaseCase
from app.models.user import User
from app.forms import *
from app.db import session
from flask_login import current_user

class UserAuthTests(BaseCase):
    def createUser(self):
        user = User(username = 'Juniper', password = 'password')
        user.set_password('password')
        session.add(user)
        session.commit()
        
        return user
    
    
    def test_users_can_login(self):
        user = self.createUser()
        
        login = LoginForm(username = 'Juniper',
            password = 'password'
        )
        
        with self.client:
            response = self.client.post(url_for(
                    'nonAuth.login'
                ), 
                data=login.data
            )
            
            self.assertRedirects(response, url_for('auth.index'))
            self.assertTrue(current_user.username == 'Juniper')
            self.assertFalse(current_user.is_anonymous)
    
    
    def test_user_cannot_login_with_invalid_credentials(self):
        user = self.createUser()
        
        login = LoginForm(username = 'Juniper',
            password = 'secret'
        )
         
        with self.client:
            response = self.client.post(url_for(
                    'nonAuth.login'
                ),
                data = login.data
            )
            self.assertRedirects(response, url_for('nonAuth.login'))
            self.assertTrue(current_user.is_anonymous)
            
            
    def test_user_can_logout(self):
        user = self.createUser()
        login = LoginForm(username = 'Juniper',
            password = 'password'
        )
        
        with self.client:
            self.client.post(url_for('nonAuth.login'), data = login.data)
            self.client.get(url_for('auth.logout'))
            
            self.assertTrue(current_user.is_anonymous)
        
        
    def test_user_can_be_created(self):
        user = self.createUser()
        
        role = Role(
            title = 'CASHIER'
        )
        session.add(role)
        session.commit()
        login = LoginForm(username = 'Juniper',
            password = 'password'
        )
        
        with self.client:
            self.client.post(url_for('nonAuth.login'), data = login.data)
            
            response = self.client.post(
                url_for('auth.createUser'), 
                data = dict(
                    username = 'Kwaghbee',
                    password = 'secret',
                    active = 'ACTIVE',
                    role = role.id
                )
            )
            
            users = User.query.all()
            self.assertTrue(users[1].username == 'Kwaghbee')
            self.assertRedirects(response, url_for('auth.getUsers'))
        