from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework import serializers
from core.models import User
from .models import Etudiant
from core.serializers import UserSerializer

class Etudiants(ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Etudiant
        fields = '__all__'
        depth = 1

class EtudiantSerializer(ModelSerializer):

    user = UserSerializer()
    cne = serializers.CharField(max_length=255)

    class Meta:
        model = Etudiant
        fields = '__all__'
        depth = 1


    def create(self, validated_data):
        ## Creating the user
        user_data = validated_data.pop('user')
        serializer = UserSerializer(data=user_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user = User.objects.filter(pk=serializer.data["id"]).first()
        validated_data['user'] = user.id
        ## Creating The student
        serializer = EtudiantUserIdSerializer(data=validated_data)
        if not serializer.is_valid():
            User.objects.filter(pk=user.id).delete()
            raise serializers.ValidationError(serializer.errors) 
        serializer.save()

        # Representation of the data created
        data = serializer.data
        data["user"] = user

        return data


    def update(self, instance, validated_data):
        
        user_data = validated_data.pop('user')
        user = instance.user
        
        ## Update Student Data
        instance.image = validated_data.get('image', instance.image)
        instance.dateNaissance = validated_data.get('dateNaissance', instance.dateNaissance)
        instance.VilleDepart = validated_data.get('VilleDepart', instance.VilleDepart)

        instance.cne = validated_data.get('cne', instance.cne)
        instance.save()

        ## Update the user
        user.first_name = user_data.get('first_name', user.first_name)
        user.last_name = user_data.get('last_name', user.last_name)
        user.email = user_data.get('email', user.email)
        user.nationality = user_data.get('nationality', user.nationality)

        user.role = user_data.get('role', user.role)
        user.save()

        return instance
    
class EtudiantUserIdSerializer(ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=False)
    class Meta:
        model = Etudiant
        fields = '__all__'
        depth = 1 
