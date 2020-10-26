from flask import url_for
from app.db import session
from app.models.role import Role
from app.tests.base import BaseCase
from app.forms import *
from app.controllers import SystemController

class UserRoleTests(BaseCase):
    def test_role_can_be_created(self):
        user = self.createUser()
        login = self.loginUser()
        
        role_form = RoleForm(title = 'Cashier')
        
        with self.client:
            self.client.post(url_for('nonAuth.login'), data = login.data)
            response = self.client.post(url_for('auth.createRole'), data = role_form.data, follow_redirects=True)
            
            roles = Role.query.all()
            self.assertEqual(roles[0].title, 'Cashier')
            assert b'Role created Successfully!' in response.data

            

    def test_role_already_exists(self):
        user = self.createUser()
        login = self.loginUser()
        existing_role = self.createUserRole()
        
        role_form = RoleForm(title = 'Cashier')
        
        with self.client:
            self.client.post(url_for('nonAuth.login'), data = login.data)
            response = self.client.post(url_for('auth.createRole'), data = role_form.data, follow_redirects=True)
            
            assert b'Role already exists!' in response.data

            
    def test_role_can_be_updated(self):
        user = self.createUser()
        login = self.loginUser()
        role = self.createUserRole()
        
        role_form = RoleForm(title = 'Cashier 1')
        
        with self.client:
            self.client.post(url_for('nonAuth.login'), data = login.data)
            response = self.client.post(url_for('auth.updateRole', id = 1), data = role_form.data, follow_redirects=True)
            
            roles = Role.query.all()
            self.assertEqual(roles[0].title, 'Cashier 1')
            assert b'Role updated Successfully!' in response.data

        
        
    def test_role_can_be_deleted(self):
        user = self.createUser()
        login = self.loginUser()
        role = self.createUserRole()
        
        with self.client:
            self.client.post(url_for('nonAuth.login'), data = login.data)
            response = self.client.post(url_for('auth.deleteRole', id = 1), follow_redirects=True)
            
            roles = Role.query.all()
            
            self.assertTrue(roles == [])
            assert b'Role deleted Successfully!' in response.data