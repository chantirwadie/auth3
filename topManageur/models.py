from django.db import models
from core.models import User


class TopManageur(models.Model):
    image=models.ImageField(default='images/default.png',upload_to='images/')
    user = models.OneToOneField(User,related_name="topmanageur_profile", on_delete=models.CASCADE)
    dateNaissance = models.CharField(max_length=50, null=True)
    VilleDepart= models.CharField(max_length=50, null=True)
