from core.models import User
from core.authentification import decode_access_token, decode_refresh_token, create_access_token
from rest_framework import exceptions

def handleJwtVerification(token, request):
    access_token = ""
    user = None
    # Verify The Access token
    try:
        id = decode_access_token(token)
        user = User.objects.filter(pk=int(id)).first()
    except:
        try:
            refresh_token = request.COOKIES["refresh_token"]
            id = decode_refresh_token(refresh_token)
            user = User.objects.filter(pk=int(id)).first()
            access_token = create_access_token(id)
        except:
            raise exceptions.AuthenticationFailed("Unauthenticated")      
    return (user, access_token)    

