# Create your models here.
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class UserManager(BaseUserManager):

    def create_user(
        self,
        email,
        user_name,
        password=None,
        **extra_fields
    ):

        if not email:
            raise ValueError("Email field is required")

        if not user_name:
            raise ValueError("User name field is required")

        email = self.normalize_email(email)

        user = self.model(
            email=email,
            user_name=user_name,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(
        self,
        email,
        user_name,
        password=None,
        **extra_fields
    ):

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("role", User.Roles.ADMIN)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")

        return self.create_user(
            email=email,
            user_name=user_name,
            password=password,
            **extra_fields
        )

class User(AbstractBaseUser, PermissionsMixin):
    username = None
    email = models.EmailField(unique=True)
    user_name = models.CharField(max_length=150, unique=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    profile_image = models.ImageField(upload_to="profiles/", null=True, blank=True)
    # Chat-specific fields
    is_online = models.BooleanField(default=False)
    last_seen = models.DateTimeField(null=True, blank=True)
    
    class Roles(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        CUSTOMER = "CUSTOMER", "Customer"
    role = models.CharField(max_length=50, default=Roles.CUSTOMER, choices=Roles.choices)  # e.g., customer, admin, moderator


    # Django required fields
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = "email"      # login with email
    REQUIRED_FIELDS = ["user_name"]

    def __str__(self):
        return self.email
