# Generated by Django 4.0.2 on 2022-05-03 20:25

import core.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_user_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='image',
            field=models.ImageField(default='images/default.png', upload_to=core.models.upload_path),
        ),
    ]