# Generated by Django 4.0.2 on 2022-05-03 14:24
# Generated by Django 4.0.2 on 2022-05-03 18:55

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('resetPassword', '0003_alter_resetpassword_expired_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resetpassword',
            name='expired_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 3, 19, 10, 32, 248936, tzinfo=utc)),
        ),
    ]
