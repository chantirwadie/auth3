from django.db import models
from core.models import User


class Coordinateur(models.Model):

    # List of choices that defines the type of professors
    TYPE_CHOICES = (
        ('Permanent', 'Permanent'),
        ('Affilié', 'Affilié'),
        ('Vacataire','Vacataire'),
        ('Prestataire', 'Prestataire')
    )
    image=models.ImageField(default='images/default.png',upload_to='images/')

    user = models.OneToOneField(User,related_name="coordinateur_profile", on_delete=models.CASCADE)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES, null=True)
    dateNaissance = models.CharField(max_length=50, null=True)
    grade = models.CharField(max_length=50, null=True)
    DernierDiplomeUniversitaire= models.CharField(max_length=50, null=True)
    VilleDepart= models.CharField(max_length=50, null=True)
    departement = models.IntegerField()
