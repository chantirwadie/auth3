# Generated by Django 4.0.2 on 2022-05-03 14:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('etudiant', '0002_etudiant_villedepart_etudiant_datenaissance'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='etudiant',
            name='VilleDepart',
        ),
        migrations.RemoveField(
            model_name='etudiant',
            name='dateNaissance',
        ),
    ]
