from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models

# from django.contrib.postgres.fields import ArrayField  # Only if you use PostgreSQL

USERTYPE = [
    ("RO", "Regional office"),
    ("OO", "Operating office"),
]


class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("The Username must be set")
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(username, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    ro_code = models.CharField(max_length=255, blank=True, null=True, default="050000")
    oo_code = models.CharField(
        "Operating office code", max_length=255, blank=True, null=True
    )
    username = models.CharField(max_length=150, unique=True)
    user_type = models.CharField(
        choices=USERTYPE,
        max_length=50,
        blank=True,
        null=True,
    )
    reset_password = models.BooleanField(default=False)
    last_login = models.DateTimeField(blank=True, null=True)

    # Use ArrayField only with PostgreSQL
    #   role = ArrayField(models.CharField(max_length=50), blank=True, default=list)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username
