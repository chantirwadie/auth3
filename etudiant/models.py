from django.db import models
from django.db import models
from core.models import User
# Create your models here.

class Etudiant(models.Model):

    # Relation to user 
    user = models.OneToOneField(User,related_name="etudiant_profile", on_delete=models.CASCADE)
    image=models.ImageField(default='images/default.png',upload_to='images/')

    # CNE 
    cne = models.CharField(max_length=10, unique=True, blank=False, error_messages={
        "unique" : "CNE must be unique"
    })
    dateNaissance = models.CharField(max_length=50, null=True)
    VilleDepart= models.CharField(max_length=50, null=True)




    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
