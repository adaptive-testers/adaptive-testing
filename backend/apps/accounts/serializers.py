from __future__ import annotations

from typing import TYPE_CHECKING, Any

from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import User

if TYPE_CHECKING:
    from django.contrib.auth.models import AbstractBaseUser


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.

    Handles:
    - Email validation and uniqueness
    - Password validation and confirmation
    - Role validation
    - Password hashing
    """

    password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "password", "role"]

    def validate_email(self, value: str) -> str:
        value = value.lower().strip()
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def validate_role(self, value: str) -> str:
        if value.lower().strip() not in ("admin", "instructor", "student"):
            raise serializers.ValidationError(
                "Invalid role. Must be one of: admin, instructor, student."
            )
        return value

    def create(self, validated_data: dict[str, Any]) -> User:
        return User.objects.create_user(**validated_data)


class UserLoginSerializer(serializers.ModelSerializer):
    """
    Serializer for user login.

    Validates:
    - presence of email/password
    - normalizes email
    - authenticates against the backend
    """

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, trim_whitespace=False)

    # Set after successful validation
    user: User | None = None

    class Meta:
        model = User
        fields = ["email", "password"]

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        email_raw = attrs.get("email")
        password = attrs.get("password")

        if not email_raw:
            raise serializers.ValidationError({"email": "This field is required."})
        if not password:
            raise serializers.ValidationError({"password": "This field is required."})

        email = str(email_raw).strip().lower()

        request = self.context.get("request")
        auth_user: AbstractBaseUser | None = authenticate(
            request, username=email, password=password
        )

        if not auth_user:
            raise serializers.ValidationError({"detail": "Invalid credentials."})
        if not auth_user.is_active:
            raise serializers.ValidationError({"detail": "User inactive."})

        # Ensure it’s our custom User model
        if not isinstance(auth_user, User):
            raise serializers.ValidationError({"detail": "Invalid credentials."})

        self.user = auth_user  # mypy is satisfied after isinstance() narrowing
        attrs["email"] = email  # normalized
        return attrs


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for user profile."""

    class Meta:
        model = User
        fields = [
            "email",
            "first_name",
            "last_name",
            "role",
            "is_verified",
            "created_at",
        ]
        read_only_fields = ["email", "created_at"]
