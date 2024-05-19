from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUserManager(UserManager):
    """
    Custom user manager where email is the unique identifier
    for authentication instead of usernames.
    """
    # Ensure the manager is used in migrations
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        # Create user instance
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """
        Create and save a regular user with the given email and password.
        """
        # Ensure is_staff is False
        extra_fields.setdefault('is_staff', False)
        # Ensure superuser is False
        extra_fields.setdefault('is_superuser', False)
        # Create regular user
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and save a superuser with the given email and password.
        """
        # Ensure is_staff is True
        extra_fields.setdefault('is_staff', True)
        # Ensure superuser is True
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
    # Disable the username field
    username = None
    # Make email unique
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    # Required fields besides email and password
    REQUIRED_FIELDS = []

    # Use CustomUserManager for user management
    objects = CustomUserManager()

    def __str__(self):
        return self.email
