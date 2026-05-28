# Create your models here.
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models


# class UserManager(BaseUserManager):
#     def create_user(self, email, username, password=None, phone_number=None, **extra_fields):
#         if not email:
#             raise ValueError("Email is required")

#         email = self.normalize_email(email)
#         user = self.model(email=email, username=username, phone_number=phone_number, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, email, username, password=None, phone_number=None, **extra_fields):
#         user = self.create_user(email, username, password, phone_number, **extra_fields)
#         user.is_staff = True
#         user.is_superuser = True
#         user.save(using=self._db)
#         return user
class UserManager(BaseUserManager):

    def create_user(
        self,
        email,
        username,
        password=None,
        **extra_fields
    ):
        """
        Create and return a regular user.
        """

        if not email:
            raise ValueError("Email field is required")

        if not username:
            raise ValueError("Username field is required")

        email = self.normalize_email(email)

        user = self.model(
            email=email,
            username=username,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(
        self,
        email,
        username,
        password=None,
        **extra_fields
    ):
        """
        Create and return a superuser.
        """

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("role", "admin")

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")

        user = self.create_user(
            email=email,
            username=username,
            password=password,
            **extra_fields
        )

        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)

    # Chat-specific fields
    is_online = models.BooleanField(default=False)
    last_seen = models.DateTimeField(null=True, blank=True)
    profile_image = models.ImageField(upload_to="profiles/", null=True, blank=True)
    
    class Roles(models.TextChoices):
        USER = "user", "User"
        ADMIN = "admin", "Admin"
    role = models.CharField(max_length=50, default="user", choices=Roles.choices)  # e.g., user, admin, moderator
    

    # Django required fields
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = "email"      # login with email
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email