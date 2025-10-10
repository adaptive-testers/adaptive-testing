"""
Tests for the UserRegistrationSerializer and UserLoginSerializer.
"""

from typing import cast

import pytest
from django.contrib.auth import get_user_model

from apps.accounts.models import User
from apps.accounts.serializers import (
    UserLoginSerializer,
    UserRegistrationSerializer,
)

UserModel = cast(type[User], get_user_model())

pytestmark = pytest.mark.django_db


# ===============================
# UserLoginSerializer tests
# ===============================
class TestUserLoginSerializer:
    def test_valid_credentials_normalizes_email_and_sets_user(self):
        user = UserModel.objects.create_user(
            email="login@example.com",
            password="StrongP@ssw0rd!",
            first_name="Log",
            last_name="In",
            role="student",
        )
        s = UserLoginSerializer(
            data={"email": "  LOGIN@EXAMPLE.COM  ", "password": "StrongP@ssw0rd!"},
            context={"request": None},
        )
        assert s.is_valid(), s.errors
        assert s.validated_data["email"] == "login@example.com"
        assert getattr(s, "user", None) == user

    def test_invalid_credentials_returns_detail_error(self):
        UserModel.objects.create_user(
            email="badpass@example.com",
            password="CorrectPass123!",
            first_name="Bad",
            last_name="Cred",
            role="student",
        )
        s = UserLoginSerializer(
            data={"email": "badpass@example.com", "password": "wrong"},
            context={"request": None},
        )
        assert not s.is_valid()
        assert "detail" in s.errors

    def test_missing_email_or_password(self):
        # Missing both
        s = UserLoginSerializer(data={}, context={"request": None})
        assert not s.is_valid()
        assert "email" in s.errors and "password" in s.errors

        # Missing password
        s = UserLoginSerializer(
            data={"email": "x@example.com"}, context={"request": None}
        )
        assert not s.is_valid()
        assert "password" in s.errors

        # Missing email
        s = UserLoginSerializer(
            data={"password": "abc"}, context={"request": None}
        )
        assert not s.is_valid()
        assert "email" in s.errors

    def test_inactive_user_is_rejected(self):
        user = UserModel.objects.create_user(
            email="inactive@example.com",
            password="StrongP@ssw0rd!",
            first_name="Ina",
            last_name="Ctive",
            role="student",
        )
        user.is_active = False
        user.save(update_fields=["is_active"])

        s = UserLoginSerializer(
            data={"email": "inactive@example.com", "password": "StrongP@ssw0rd!"},
            context={"request": None},
        )
        assert not s.is_valid()
        assert "detail" in s.errors  # {"detail": "User inactive."}


# ===============================
# UserRegistrationSerializer tests
# ===============================
class TestUserRegistrationSerializer:
    """Test cases for UserRegistrationSerializer."""

    @pytest.fixture
    def valid_registration_data(self):
        """Fixture providing valid user registration data."""
        return {
            "email": "test@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "password": "SecurePass123",
            "role": "student",
        }

    def test_valid_registration_data(self, valid_registration_data):
        """Serializer with valid data creates user successfully."""
        serializer = UserRegistrationSerializer(data=valid_registration_data)
        assert serializer.is_valid()

        user = serializer.save()
        assert user.email == "test@example.com"
        assert user.first_name == "John"
        assert user.last_name == "Doe"
        assert user.role == "student"
        # password is hashed
        assert user.password != valid_registration_data["password"]
        assert len(user.password) > 20

    def test_duplicate_email(self, valid_registration_data):
        """Serializer rejects duplicate email."""
        UserModel.objects.create_user(
            email="existing@example.com",
            first_name="Existing",
            last_name="User",
            password="testpass123",
            role="instructor",
        )

        duplicate = {**valid_registration_data, "email": "existing@example.com"}
        serializer = UserRegistrationSerializer(data=duplicate)
        assert not serializer.is_valid()
        assert "email" in serializer.errors
        assert "already exists" in str(serializer.errors["email"])

    def test_email_normalization(self, valid_registration_data):
        """Email is normalized to lowercase and stripped."""
        data = {**valid_registration_data, "email": "  TEST@EXAMPLE.COM  "}
        serializer = UserRegistrationSerializer(data=data)
        assert serializer.is_valid()
        user = serializer.save()
        assert user.email == "test@example.com"

    def test_all_valid_roles(self, valid_registration_data):
        """All valid roles are accepted."""
        for role in ["student", "instructor", "admin"]:
            data = {
                **valid_registration_data,
                "email": f"test_{role}@example.com",
                "role": role,
            }
            serializer = UserRegistrationSerializer(data=data)
            assert serializer.is_valid(), f"Role '{role}' should be valid"
            user = serializer.save()
            assert user.role == role

    def test_invalid_email_format(self, valid_registration_data):
        """Serializer rejects invalid email format."""
        invalid = {**valid_registration_data, "email": "invalid-email"}
        serializer = UserRegistrationSerializer(data=invalid)
        assert not serializer.is_valid()
        assert "email" in serializer.errors

    def test_invalid_role(self, valid_registration_data):
        """Serializer rejects invalid role."""
        invalid = {**valid_registration_data, "role": "invalid_role"}
        serializer = UserRegistrationSerializer(data=invalid)
        assert not serializer.is_valid()
        assert "role" in serializer.errors

    def test_weak_password(self, valid_registration_data):
        """Serializer rejects weak password."""
        invalid = {**valid_registration_data, "password": "123"}
        serializer = UserRegistrationSerializer(data=invalid)
        assert not serializer.is_valid()
        assert "password" in serializer.errors

    def test_required_fields(self):
        """All required fields (excluding optional role) are validated."""
        serializer = UserRegistrationSerializer(data={})
        assert not serializer.is_valid()

        # Only these are required by the serializer
        required = {"email", "first_name", "last_name", "password"}
        assert required.issubset(set(serializer.errors.keys()))

    def test_password_is_write_only(self, valid_registration_data):
        """Password field is write-only and not returned in data."""
        serializer = UserRegistrationSerializer(data=valid_registration_data)
        assert serializer.is_valid()
        user = serializer.save()

        assert "password" not in serializer.data
        assert user.password and user.password != valid_registration_data["password"]
