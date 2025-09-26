from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class UserAdmin(UserAdmin):
    """Admin configuration for the custom User model"""

    list_display = (
        "email",
        "first_name",
        "last_name",
        "is_verified",
        "is_active",
        "created_at",
    )
    list_filter = (
        "role",
        "is_verified",
        "is_active",
        "is_staff",
        "is_superuser",
        "created_at",
        "oauth_provider",
    )
    search_fields = ("email", "first_name", "last_name")
    ordering = ("-created_at",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_verified",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                    "role",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "created_at", "updated_at")}),
        ("OAuth", {"fields": ("oauth_provider", "oauth_id")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "first_name",
                    "last_name",
                    "password1",
                    "password2",
                ),
            },
        ),
    )

    readonly_fields = ("created_at", "updated_at", "last_login")
