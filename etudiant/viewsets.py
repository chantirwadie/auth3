from rest_framework import viewsets
from .models import Etudiant
from .  import serializers


class EtudiantViewset(viewsets.ModelViewSet):
    queryset =Etudiant.objects.all()
    serializer_class = serializers.EtudiantAddSerializer
