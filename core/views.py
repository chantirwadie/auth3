from rest_framework.views import APIView
from rest_framework import exceptions
from rest_framework.response import Response
from .serializers import ResetPasswordApiViewSerializer, UserSerializer, LoginSerializer, PasswordResetSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from auth_middelware.permissions import IsJwtAuthenticated
from rest_framework import status
from .models import User
from .authentification import create_access_token, create_refresh_token, decode_refresh_token
# Create your views here.
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.conf import settings
from resetPassword.serializers import ResetPasswordSerializer
from datetime import datetime
from django.utils.dateparse import parse_datetime
import urllib3
from resetPassword.models import ResetPassword
import pytz
from etudiant.models import Etudiant
from etudiant.serializers import EtudiantSerializer
from professeur.models import Professeur
from professeur.serializers import ProfesseurSerializer
from coordinateur.models import Coordinateur
from coordinateur.serializers import CoordinateurSerializer
from topManageur.models import TopManageur
from topManageur.serializers import TopManageurSerializer



http = urllib3.PoolManager()
class RegisterApiView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request):

        # The `validate` method on serializer handles validate the user
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Getting the id of the user

        user  = User.objects.get(email=serializer.data['email'])
        id = user.id

        user.last_login = datetime.now(pytz.timezone("Africa/Abidjan"))
        user.save()

        # Creating Tokens
        access_token = create_access_token(id)
        refresh_token = create_refresh_token(id)

        # Initiating the response
        response = Response(serializer.data, status=status.HTTP_200_OK)

        # Add the refresh token to a cookie
        response.set_cookie(key='refresh_token', value=refresh_token, httponly=True)

        # Appending the access token to the response data
        response.data["access_token"] = access_token

        return response        

class UserApiView(APIView):

    def get(self,request):
        user = request.session.get("user", None)
        if not user:
            raise exceptions.AuthenticationFailed("Unauthenticated user")

        role = user['role']

        # if role == "Etudiant":
        #     etudiant = Etudiant.objects.get(user=user['id'])
        #     return Response({"user" : user, "etudiant" : EtudiantSerializer(etudiant).data},200)
        
        # if role == "TopManageur":
        #     topManageur = TopManageur.objects.get(user=user['id'])
        #     return Response({"user" : user, "topManageur" : TopManageurSerializer(topManageur).data},200)    

        if role == "Coordinateur":
            coordinateur = Coordinateur.objects.get(user=user['id'])
            return Response({"user" : user, "coordinateur" : CoordinateurSerializer(coordinateur).data},200)     
            

        if role == "Professeur":
            professeur = Professeur.objects.get(user=user['id'])
            return Response({"user" : user, "professeur" : ProfesseurSerializer(professeur).data},200)      


        return Response({"user" : user},200)

class RefreshApiView(APIView):
    def post(self,request):
        refresh_token = request.COOKIES.get('refresh_token')
        id = decode_refresh_token(refresh_token)
        access_token = create_access_token(id)
        return Response({
            'access_token': access_token
        })
class LogoutApiView(APIView):
    def post(self, request):
        response =Response()
        response.delete_cookie(key="refresh_token")
        response.data = {
            'message': "success"
        }
        return response
        

class ForgetPasswordApiView(APIView):
    serializer_class = UserSerializer

    def post(self,request):

        email = request.data.get('email')
        if not User.objects.filter(email=email).exists():
            return Response({"error": "Pas d'utilisateur avec cette adresse email"}, status=status.HTTP_400_BAD_REQUEST) 
        user = User.objects.get(email=email)

        token = urlsafe_base64_encode(force_bytes(default_token_generator.make_token(user))) 
        data = {'user': user.id, 'token' : token}

        serializer = ResetPasswordSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        data = serializer.data

        token = data.get('token', None)
        created_at = data.get('created_at', None)
        created_at = parse_datetime(created_at)
        created_at = datetime.strftime(created_at, '%Y-%m-%d %H:%M:%S.%f')
        expired_at = data.get('expired_at', None)
        expired_at = parse_datetime(expired_at)
        expired_at = datetime.strftime(expired_at, '%Y-%m-%d %H:%M:%S.%f')
        last_name = user.last_name

        

        # Generate a one-use only link for resetting password

        link = settings.FRONTEND_URL + "/reset-password/" + token

        # Send an email to the user with the link

        backend_endpoint = settings.EMAIL_BACKEND_URL + "/api/v4/send-mail/reset-password"

        r = http.request('POST', backend_endpoint , {
            'created_at': created_at,
            'expired_at': expired_at,
            'last_name': last_name,
            'link': link,
            'email': email
        })
        
        return Response({"message": "success"})


class ResetPasswordApiView(APIView):

    def post(self, request):

        token = request.data.get('token')
        password = request.data.get('password')

        if not ResetPassword.objects.filter(token=token).exists():
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST) 

        reset_password = ResetPassword.objects.get(token=token)

        if reset_password.expired_at < datetime.now().replace(tzinfo=pytz.UTC):
            return Response({"error": "Token expiré"}, status=status.HTTP_400_BAD_REQUEST)

        if  reset_password.isValidated:
            return Response({"error": "Token déjà utilisé"}, status=status.HTTP_400_BAD_REQUEST)

        
        user = User.objects.get(id=reset_password.user.id)
        user.set_password(password)
        user.save()    

        ## Update token field   

        reset_password.isValidated = True
        reset_password.save()   

        return Response({"status": status.HTTP_200_OK, "message": "success"})


# class ResetPasswordApiView(APIView):

#     def post(self, request):
#         reset_password = ResetPassword.objects.get(token=request.data.get('token'))
#         password = request.data.get('password')
#         if not reset_password:
#             return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
#         if reset_password.expired_at < datetime.now().replace(tzinfo=pytz.UTC):
#             return Response({"error": "Token expiré"}, status=status.HTTP_400_BAD_REQUEST)    
#         if password is None:
#             return Response({"error": "Mot de passe requis"}, status=status.HTTP_400_BAD_REQUEST)

#         user = User.objects.get(id=reset_password.user.id)
#         user.set_password(password)
#         user.save()

#         return Response({"status": status.HTTP_200_OK, "message": "success"})
class GeneralStatApiView(APIView):

    def get(self, request):

        nbrEtudiant = User.objects.filter(role='Etudiant').count()
        nbrProfesseur = User.objects.filter(role='Professeur').count()
        nbrCoordinateur = User.objects.filter(role='Coordinateur').count()
        nbrStaff = User.objects.filter(role='Staff').count()
        
        return Response({
            'nbrEtudiant': nbrEtudiant,
            'nbrProfesseur': nbrProfesseur,
            'nbrCoordinateur': nbrCoordinateur,
            'nbrStaff': nbrStaff
        })
        

