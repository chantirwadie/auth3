# Generated by Django 4.0.2 on 2022-05-07 11:08

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('resetPassword', '0007_alter_resetpassword_expired_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resetpassword',
            name='expired_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 7, 11, 23, 47, 92514, tzinfo=utc)),
        ),
    ]
