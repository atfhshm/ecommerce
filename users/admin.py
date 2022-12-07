from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


from users.models import User, Product

# Register your models here.
@admin.register(User)
class UserAdminConfig(UserAdmin):
    list_display = (
        "username",
        "email",
        "user_type",
        "is_active",
        "is_staff",
        "is_superuser",
        "last_login",
    )
    list_filter = ("is_active", "is_staff", "is_superuser", "user_type")
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "username",
                    "email",
                    "user_type",
                    "password",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_staff",
                    "is_active",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "user_type",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                ),
            },
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)


@admin.register(Product)
class ProductAdminConfig(admin.ModelAdmin):
    fields = ("name", "description", "price", "seller", "wishlist")
