from app.models import permission, role
from app.db import session

Permission = permission.Permission

class HasPermissionTrait:
    
    def givePermissionsTo(self, perms):
        """ Assign permissions to a user or role
            @return permissions or null
        """
        
        # permissions = self.getAllPermissions(perms) 
        if perms is None:
            return self
        
        self.permissions.extend(perms)
        session.add(self)
        session.commit()
        return self
        
        
    def revokePermissions(self, perms):
        """
            Revoke a specified permission from a user.
            Permissions are only revoked if they are in the scope any of the user's
            roles. If the permission is out of scope, a RolePermissionScopeException
            is raised.
        """
        
        if perms is not None:
            for perm in perms: 
                self.permissions.remove(perm)
                session.commit()
                return self
            return self
    
    
    def hasPermissionTo(perm):
        """Check if a user has permission to perform an action."""
        
        return self.hasPermissionThroughRole(perm) or self.hasPermission(perm)
        
        
    def hasPermissionThroughRole(perm):
        """hasPermission through role"""
        
        if type(perm) == str:
            permission = Permission.query.filter_by(name=perm.name).first()
            role = Permission.roles.first()
            roles = self.query.all()
            
            if roles.contains(role):
                return True
        else:
            for role in perm.roles:
                if roles.contains(role):
                    return True
        
        return False
    
    
    def hasRole(*roles):
        """check if user has required role"""
        
        user_roles = self.query.all()
        for role in roles:
            if user_roles.contains(role):
                return True
            return False
        
        
    # """get all permissions"""
    # @classmethod
    # def getAllPermissions(self,perms):
    #     return session.query(Permission).filter_by(Permission.slug.in_(perms)).all()
    
    def hasPermission(perm):
        """check if user has direct permissions"""
        
        permit = Permission.query.filter_by(slug = perm).first()
        if permit is None:
            return False
            raise('User does not have permission')
        return True