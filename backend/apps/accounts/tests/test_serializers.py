"""
Tests for the UserLoginSerializer.
"""

from typing import cast

import pytest
from django.contrib.auth import get_user_model

from apps.accounts.models import User
from apps.accounts.serializers import UserLoginSerializer

# Type alias for the User model
UserModel = cast(type[User], get_user_model())


@pytest.mark.django_db
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
            context={"request": None},  # authenticate() works fine with None
        )
        assert s.is_valid(), s.errors
        # email should be normalized in validated_data
        assert s.validated_data["email"] == "login@example.com"
        # serializer.user should be set to the authenticated user
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
        # Our serializer raises ValidationError({"detail": "Invalid credentials."})
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
        s = UserLoginSerializer(data={"password": "abc"}, context={"request": None})
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
        # Our serializer raises ValidationError({"detail": "User inactive."})
        assert "detail" in s.errors
