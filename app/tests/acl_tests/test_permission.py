from flask import url_for
from app.db import session
from app.models.permission import Permission
from app.tests.base import BaseCase
from app.forms import *
from app.controllers import SystemController

class UserPermissionTests(BaseCase):
    def createUserPermission(self):
        permission = Permission(name = 'Create User')
        session.add(permission)
        session.commit()
        
    
    def test_user_can_create_permission(self):
        user = self.createUser()
        login = self.loginUser()
        
        perm_form = PermissionForm(name = 'Create Product')
        
        with self.client:
            self.client.post(url_for('nonAuth.login'), data = login.data)
            response = self.client.post(url_for('auth.createPermission'), data = perm_form.data)
            
            permissions = Permission.query.all()
            self.assertEqual(permissions[0].name, 'Create Product')
            self.assertEqual(permissions[0].slug, 'create-product')
            self.assertRedirects(response, url_for('auth.getPermissions'))
            
    def test_permission_already_exists(self):
        user = self.createUser()
        login = self.loginUser()
        permission = self.createUserPermission()
        
        perm_form = PermissionForm(name = 'Create User')
        
        with self.client:
            self.client.post(url_for('nonAuth.login'), data = login.data)
            response = self.client.post(url_for('auth.createPermission'), data = perm_form.data, follow_redirects = True)
            
            assert b'Permission already exists!' in response.data
            
    def test_permission_can_update(self):
        user = self.createUser()
        login = self.loginUser()
        permission = self.createUserPermission()
        
        perm_form = PermissionForm(name = 'Create User2')
        
        with self.client:
            self.client.post(url_for('nonAuth.login'), data = login.data)
            response = self.client.post(url_for('auth.updatePermission', id = 1), data = perm_form.data)
            
            permissions = Permission.query.all()
            
            self.assertEqual(permissions[0].name, 'Create User2')
            self.assertRedirects(response, url_for('auth.getPermissions'))
            
    def test_permission_starts_with_string(self):
        user = self.createUser()
        login = self.loginUser()
        
        perm_form = PermissionForm(name = '2sss')
        
        with self.client:
            self.client.post(url_for('nonAuth.login'), data = login.data)
            response = self.client.post(url_for('auth.createPermission'), data = perm_form.data, follow_redirects = True)
            
            assert b'Value entered must start with an alphabet!' in response.data
            
    def test_permission_can_be_deleted(self):
        user = self.createUser()
        login = self.loginUser()
        permission = self.createUserPermission()
        
        with self.client:
            self.client.post(url_for('nonAuth.login'), data = login.data)
            response = self.client.post(url_for('auth.deletePermission', id = 1))
            
            permissions = Permission.query.all()
            
            self.assertTrue(permissions == [])
            self.assertRedirects(response, url_for('auth.getPermissions'))
