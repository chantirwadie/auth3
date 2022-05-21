import datetime
from django.db import models
from core.models import User
import pytz

# Create your models here.


class ResetPassword(models.Model):

    user = models.ForeignKey(User,related_name="reset_password_profile", on_delete=models.CASCADE)
    token = models.CharField(max_length=255)
    isValidated = models.BooleanField(default=False)
    expired_at = models.DateTimeField(default=datetime.datetime.now(tz=pytz.UTC)+datetime.timedelta(minutes=15))
    created_at = models.DateTimeField(auto_now_add=True)