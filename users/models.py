from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from django.utils import timezone


class UserTypes(models.TextChoices):
    SELLER = ("SELLER", "Seller")
    BUYER = ("BUYER", "Buyer")
    STAFF = ("STAFF", "Staff")


class UserManager(BaseUserManager):
    def create_user(self, username, email, password, **extra_fields):
        if not email:
            raise ValueError("email must be provided.")
        if not username:
            raise ValueError("username must be provided.")

        email = self.normalize_email(email)

        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("user_type", UserTypes.STAFF)

        return self.create_user(
            username=username, email=email, password=password, **extra_fields
        )


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField("first name", max_length=150, blank=True, null=True)
    last_name = models.CharField("last name", max_length=150, blank=True, null=True)
    username = models.CharField("username", max_length=150, unique=True)
    email = models.EmailField("email", max_length=150, unique=True)
    is_staff = models.BooleanField("staff status", default=False)
    is_active = models.BooleanField("active", default=True)
    date_joined = models.DateTimeField("date joined", default=timezone.now)
    user_type = models.CharField(
        "user type", choices=UserTypes.choices, max_length=8, default=UserTypes.STAFF
    )

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        db_table = "users"

    def __str__(self) -> str:
        return self.username


class Product(models.Model):
    name = models.CharField("product name", max_length=150, unique=True)
    description = models.CharField("description", max_length=200)
    price = models.IntegerField("price")
    seller = models.ForeignKey(
        User, related_name="products", on_delete=models.CASCADE, default=None
    )
    wishlist = models.ManyToManyField(User, related_name="wishlist", blank=True)

    class Meta:
        db_table = "products"

    def __str__(self):
        return self.name
