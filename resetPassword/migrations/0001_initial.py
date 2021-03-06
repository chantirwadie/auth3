# Generated by Django 4.0.2 on 2022-05-02 04:01

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ResetPassword',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=255)),
                ('isValidated', models.BooleanField(default=False)),
                ('expired_at', models.DateTimeField(default=datetime.datetime(2022, 5, 2, 4, 16, 40, 71078))),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='reset_password_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
