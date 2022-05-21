from rest_framework import permissions
from django.core.exceptions import PermissionDenied


class IsJwtAuthenticated(permissions.BasePermission):
    
    def has_permission(self, request, view):
        user = request.session.get('user', None)
        self.message = "Not Authenticated"
        if user:
            return True
        return False 

class IsEtudiant(permissions.BasePermission):
    message = "Student Not authenticated"

    def has_permission(self,request, view):
        user = request.session.get('user', None)
        if not user:
            return False

        if not user['role'] == "Etudiant":
            return False
            
        return True       