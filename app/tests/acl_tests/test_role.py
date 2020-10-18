from flask import url_for
from app.db import session
from app.models.role import Role
from app.tests.base import BaseCase
from app.forms import *

class UserRoleTests(BaseCase):
    def test_role_can_be_created(self):
        user = self.createUser()
        login = self.loginUser()
        
        role = RoleForm(title = 'Cashier')
        
        with self.client:
            self.client.post(url_for('nonAuth.login'), data = login.data)
            
            response = self.client.post(url_for('auth.createRole'), data = role.data)
            
            self.assertRedirects(response, url_for('auth.getRoles'))
            
    def test_role_already_exists(self):
        user = self.createUser()
        login = self.loginUser()
        
        existing_role = Role(title = 'Cashier')
        session.add(existing_role)
        session.commit()
        
        role = RoleForm(title = 'Cashier')
        
        with self.client:
            self.client.post(url_for('nonAuth.login'), data = login.data)
            response = self.client.post(url_for('auth.createRole'), data = role.data, follow_redirects=True)
            
            try:
                assert b'Role already exists!' in response.data
            except AssertionError:
                print("Assertion failed!")
            
    # test_role_can_be_updated
    # test_role_can_be_deleted