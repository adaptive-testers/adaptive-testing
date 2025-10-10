from __future__ import annotations

from typing import Any

from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import UserManager


class UserRole(models.TextChoices):
    ADMIN = "admin", "Admin"
    INSTRUCTOR = "instructor", "Instructor"
    STUDENT = "student", "Student"


class User(AbstractUser):
    # Remove username; use email as identifier
    username = None

    email = models.EmailField(unique=True, help_text="User's email address (used as username)")
    first_name = models.CharField(max_length=150, blank=False)
    last_name = models.CharField(max_length=150, blank=False)

    role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.STUDENT,
        help_text="User's role in the system",
    )

    is_verified = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: list[str] = []

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}".strip()

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

    def clean(self) -> None:
        super().clean()
        if self.email:
            self.email = self.email.strip().lower()

    def save(self, *args: Any, **kwargs: Any) -> None:
        if self.email:
            self.email = self.email.strip().lower()
        super().save(*args, **kwargs)
