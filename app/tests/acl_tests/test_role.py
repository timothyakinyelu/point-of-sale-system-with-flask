from flask import url_for
from app.db import session
from app.models.role import Role
from app.tests.base import BaseCase
from app.forms import *
from app.controllers import SystemController

class UserRoleTests(BaseCase):
    def createUserRole(self):
        role = Role('Cashier')
        session.add(role)
        session.commit()
        
        return role

    
    def test_role_can_be_created(self):
        user = self.createUser()
        login = self.loginUser()
        
        role_form = RoleForm(title = 'Cashier')
        
        with self.client:
            self.client.post(url_for('nonAuth.login'), data = login.data)
            response = self.client.post(url_for('auth.createRole'), data = role_form.data)
            
            roles = Role.query.all()
            self.assertEqual(roles[0].title, 'Cashier')
            self.assertRedirects(response, url_for('auth.getRoles'))
            

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
            response = self.client.post(url_for('auth.updateRole', id = 1), data = role_form.data)
            
            roles = Role.query.all()
            self.assertEqual(roles[0].title, 'Cashier 1')
            self.assertRedirects(response, url_for('auth.getRoles'))
        
        
    def test_role_can_be_deleted(self):
        user = self.createUser()
        login = self.loginUser()
        role = self.createUserRole()
        
        with self.client:
            self.client.post(url_for('nonAuth.login'), data = login.data)
            response = self.client.post(url_for('auth.deleteRole', id = 1))
            
            roles = Role.query.all()
            
            self.assertTrue(roles == [])
            self.assertRedirects(response, url_for('auth.getRoles'))