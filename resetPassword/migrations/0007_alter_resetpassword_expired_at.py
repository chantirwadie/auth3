# Generated by Django 4.0.2 on 2022-05-05 01:17

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('resetPassword', '0006_alter_resetpassword_expired_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resetpassword',
            name='expired_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 5, 1, 32, 57, 269156, tzinfo=utc)),
        ),
    ]