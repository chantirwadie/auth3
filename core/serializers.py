from dataclasses import fields
from rest_framework.serializers import ModelSerializer
from .models import User
from rest_framework import serializers
from django.contrib.auth import authenticate 
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from resetPassword.serializers import ResetPasswordSerializer




class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email','cin', 'nationality','password', 'role']
        fields = ['id', 'first_name', 'last_name', 'email','cin','nationality','password', 'role']
        extra_kwargs = {
            'password': {'write_only': True}
        }
   

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        instance = self.Meta.model(**validated_data)

        instance.username = instance.email

        if password is not None:
            instance.set_password(password)
        else:
            instance.set_password(instance.first_name+instance.last_name)    

        instance.save()
        return instance
        
class LoginSerializer(serializers.Serializer):
    
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)

    def validate(self, data):
        # The `validate` method is where we make sure that the current
        # instance of `LoginSerializer` has "valid". In the case of logging a
        # user in, this means validating that they've provided an email
        # and password and that this combination matches one of the users in
        # our database.
        email = data.get('email', None)
        password = data.get('password', None)

        # Raise an exception if an
        # email is not provided.
        if email is None:
            raise serializers.ValidationError(
                'An email address is required to log in.'
            )

        # Raise an exception if a
        # password is not provided.
        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )

        # The `authenticate` method is provided by Django and handles checking
        # for a user that matches this email/password combination. Notice how
        # we pass `email` as the `username` value since in our User
        # model we set `USERNAME_FIELD` as `email`.
        user = authenticate(username=email, password=password)

        # If no user was found matching this email/password combination then
        # `authenticate` will return `None`. Raise an exception in this case.
        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found.'
            )

        # Django provides a flag on our `User` model called `is_active`. The
        # purpose of this flag is to tell us whether the user has been banned
        # or deactivated. This will almost never be the case, but
        # it is worth checking. Raise an exception in this case.
        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )

        # The `validate` method should return a dictionary of validated data.
        # This is the data that is passed to the `create` and `update` methods
        # that we will see later on.

        us = UserSerializer(user).data

        return {
            'email': user.email,
        }        


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2, max_length=255)

    def validate(self, attrs):
        email = attrs['email']
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Pas d'utilisateur avec cette adresse email")
        return attrs

    def create(self, validated_data):
        email = validated_data.get('email')
        user = User.objects.get(email=email)

        token = urlsafe_base64_encode(force_bytes(default_token_generator.make_token(user)))

        data = {'user' :user.id, 'token' :token}
        serializer = ResetPasswordSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        ## Save the data in the object

        validated_data['data'] = serializer.data

        return validated_data



class ResetPasswordApiViewSerializer(serializers.Serializer):

    user = UserSerializer()
    password = serializers.CharField(max_length=225)

    class Meta:
        fields = "__all__"


    def create(self, validated_data):
        password = validated_data.get('password')
        user = validated_data.get('user')
        user = User.objects.get(id=user['id'])
        print(user.first_name)
        user.set_password(password)
        user.save()
        return validated_data    