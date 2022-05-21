from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework import serializers
from .models import ResetPassword
from core.models import User
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes


class ResetPasswordSerializer(ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=False)

    class Meta:
        model = ResetPassword
        fields = '__all__'
        depth = 1


    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)      
        instance.save()
        return instance    


    