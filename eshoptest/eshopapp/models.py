from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils.translation import gettext_lazy as _

class CustomUserManager(UserManager):
    """
    Custom user manager where email is the unique identifier
    for authentication instead of usernames.
    """
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions using email as the username.
    """
    username = None  # Disable the username field
    email = models.EmailField(_('email address'), unique=True)  # Make email unique

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Required fields besides email and password

    objects = CustomUserManager()

    def __str__(self):
        return self.email
