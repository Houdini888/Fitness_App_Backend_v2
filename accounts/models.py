from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):
    def create_user(self, email, password = None, **extra_fields):
        # Normalize the email address
        email = self.normalize_email(email)

        if not password:
            raise ValueError('Password is required!')

        # Create a new User instance
        user = self.model(email=email, **extra_fields)

        # Set the password
        user.set_password(password)

        # Save the User object
        user.save()

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        # Create a regular user first
        user = self.create_user(email, password, **extra_fields)

        # Set the user as a superuser
        user.is_superuser = True
        user.is_staff = True

        # Save the User object
        user.save()

        return user

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)

    password = models.CharField(max_length=255)

    GENDER_CHOICES = [('M', 'Male'), ('F', 'Female')]
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)

    date_of_birth = models.DateField()
    weight = models.IntegerField()
    height = models.DecimalField(max_digits=5, decimal_places=2)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def update_details(self, gender, date_of_birth, weight, height):
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.weight = weight
        self.height = height
