from __future__ import annotations

from typing import Any, ClassVar

from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import UserManager


class UserRole(models.TextChoices):
    ADMIN = "admin", "Admin"
    INSTRUCTOR = "instructor", "Instructor"
    STUDENT = "student", "Student"


class User(AbstractUser):
    """Custom user model using email as the username field."""

    # Remove the username field from AbstractUser
    username: ClassVar[None] = None

    email = models.EmailField(
        unique=True,
        db_index=True,
        help_text="User's email address (used as username)",
    )
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)

    role = models.CharField(
        max_length=32,
        choices=UserRole.choices,
        default=UserRole.STUDENT,
        help_text="User's role in the system",
    )
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    # Typed manager
    objects: UserManager = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    @property
    def full_name(self) -> str:
        return f"{(self.first_name or '').strip()} {(self.last_name or '').strip()}".strip()

    @property
    def display_name(self) -> str:
        return self.full_name or self.email

    @property
    def is_student(self) -> bool:
        return bool(self.role == UserRole.STUDENT)

    @property
    def is_instructor(self) -> bool:
        return bool(self.role == UserRole.INSTRUCTOR)

    @property
    def is_admin(self) -> bool:
        return bool(self.role == UserRole.ADMIN)

    # --- Normalization ---
    def save(self, *args: Any, **kwargs: Any) -> None:
        # Ensure email is always stored in lowercase and trimmed.
        if self.email:
            self.email = self.email.strip().lower()
        super().save(*args, **kwargs)

    def __str__(self) -> str:  # pragma: no cover
        return str(self.email)
