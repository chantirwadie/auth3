from django.db import models

from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.db import models
def upload_path(instance,filename):
    return 'images/{filename}'.format(filename=filename)


class UserManager(BaseUserManager):
    """
    Django requires that custom users define their own Manager class. By
    inheriting from `BaseUserManager`, we get a lot of the same code used by
    Django to create a `User`. 

    All we have to do is override the `create_user` function which we will use
    to create `User` objects.
    """
    def create_user(self, username, email, password=None):
        """Create and return a `User` with an email, username and password."""
        if email is None:
            raise TypeError('Users must have an email.')

        username = email
        user = self.model(username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user


    def create_superuser(self,username, email, password):
        """
        Create and return a `User` with superuser (admin) permissions.
        """
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user

class User(AbstractBaseUser, PermissionsMixin):

    # The list of available roles
    ROLES = (
        ('Etudiant', 'Etudiant'),
        ('Coordinateur', 'Coordinateur'),
        ('Staff', 'Staff'),
        ('TopManageur', 'TopManageur'),
        ('Professeur', 'Professeur')
    )

    
    first_name = models.CharField(max_length=120, blank=True)
    last_name = models.CharField(max_length=120, blank=True)

    # Each `User` needs a human-readable unique identifier that we can use to
    # represent the `User` in the UI. We want to index this column in the
    # database to improve lookup performance.
    username = models.CharField(db_index=True, max_length=255, unique=True, error_messages={
        "unique" : "The field Must be unique"
    })
    
    image=models.ImageField(default='images/default.png',upload_to=upload_path,)

    # We also need a way to contact the user and a way for the user to identify
    # themselves when logging in. Since we need an email address for contacting
    # the user anyways, we will also use the email for logging in because it is
    # the most common form of login credential at the time of writing.
    email = models.EmailField(db_index=True, unique=True, error_messages={
        "unique" : "L'email existe deja"
    })

    # CIN for national idendity
    cin = models.CharField(max_length=12, blank=True, unique=False, error_messages={
        "unique" : "CIN must be unique"
    })

    # Nationality
    nationality = models.CharField(blank=True, max_length=60)

    # When a user no longer wishes to use our platform, they may try to delete
    # their account. That's a problem for us because the data we collect is
    # valuable to us and we don't want to delete it. We
    # will simply offer users a way to deactivate their account instead of
    # letting them delete it. That way they won't show up on the site anymore,
    # but we can still analyze the data.
    is_active = models.BooleanField(default=True)

    # The `is_staff` flag is expected by Django to determine who can and cannot
    # log into the Django admin site. For most users this flag will always be
    # false.
    is_staff = models.BooleanField(default=False)

    # Role field is used to identify the nature of the user for navigability reasons
    # Ex: Staff -> Look up the foreign key in the staff model
    role = models.CharField(max_length=50, choices=ROLES, null=True)

    # A Date of Birth field for users

    # A timestamp representing when this object was created.
    created_at = models.DateTimeField(auto_now_add=True)

    # A timestamp reprensenting when this object was last updated.
    updated_at = models.DateTimeField(auto_now=True)

    # More fields required by Django when specifying a custom user model.

    # The `USERNAME_FIELD` property tells us which field we will use to log in.
    # In this case we want it to be the email field.
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    # Tells Django that the UserManager class defined above should manage
    # objects of this type.
    objects = UserManager()

    def __str__(self):
        """
        Returns a string representation of this `User`.

        This string is used when a `User` is printed in the console.
        """
        return self.email



       