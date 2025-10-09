from __future__ import annotations

from typing import TYPE_CHECKING, Any, cast

from django.contrib.auth.models import BaseUserManager

if TYPE_CHECKING:
    from .models import User


class UserManager(BaseUserManager["User"]):
    """Custom user manager for the User model"""

    def create_user(
        self,
        email: str,
        password: str | None = None,
        **extra_fields: Any,
    ) -> User:
        """Create and save a user with the given email and password"""
        if not email:
            raise ValueError("The Email field must be set")

        email = self.normalize_email(email)
        # BaseUserManager.model is typed loosely; cast to our concrete model for mypy
        user = cast("User", self.model(email=email, **extra_fields))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self,
        email: str,
        password: str | None = None,
        **extra_fields: Any,
    ) -> User:
        """Create and return a superuser with the given email and password"""

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)
