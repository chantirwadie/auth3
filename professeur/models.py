from django.db import models
from core.models import User


class Professeur(models.Model):
    
    def upload_path(instance,filename):
        return 'images/{filename}'.format(filename=filename)
    # List of choices that defines the type of professors
    TYPE_CHOICES = (
        ('Permanent', 'Permanent'),
        ('Affilié', 'Affilié'),
        ('Vacataire','Vacataire'),
        ('Prestataire', 'Prestataire')
    )
    image=models.ImageField(default='images/default.png',upload_to='images/')

    user = models.OneToOneField(User,related_name="professeur_profile", on_delete=models.CASCADE)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES, null=True)
    dateNaissance = models.CharField(max_length=50, null=True)
    grade = models.CharField(max_length=50, null=True)
    DernierDiplomeUniversitaire= models.CharField(max_length=50, null=True)
    Specialite = models.CharField(max_length=50, null=True)
    VilleDepart= models.CharField(max_length=50, null=True)
    ModulesEnseignes = models.CharField(max_length=50, null=True)
    departement = models.IntegerField(null=True)
