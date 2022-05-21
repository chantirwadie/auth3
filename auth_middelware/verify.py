import jwt
from rest_framework.authentication import BaseAuthentication
from django.middleware.csrf import CsrfViewMiddleware
from rest_framework import exceptions
from django.conf import settings
from core.models import User
from .jwtHandler import handleJwtVerification

class CSRFCheck(CsrfViewMiddleware):
    def _reject(self, request, reason):
        return reason

class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        user = None
        authorization_heaader = request.headers.get('Authorization')

        if not authorization_heaader:
            return None
        access_token = authorization_heaader.split(' ')[1]    
        try:
            (user, access_token) = handleJwtVerification(access_token)
            self.enforce_csrf(request)
            return (user, None)  
        except:
            return None      
    def enforce_csrf(self, request):
        check = CSRFCheck(request)
        check.process_request(request)
        reason = check.process_view(request, None, (), {})
        print(reason)
        if reason:
            raise exceptions.PermissionDenied('CSRF Failed: %s' % reason)  