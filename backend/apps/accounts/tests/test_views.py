from typing import cast

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.accounts.models import User

UserModel = cast(type[User], get_user_model())

pytestmark = pytest.mark.django_db


class TestUserLoginView:
    def test_login_success_returns_tokens_and_profile(self):
        user = UserModel.objects.create_user(
            email="loginok@example.com",
            password="StrongP@ssw0rd!",
            first_name="Log",
            last_name="In",
            role="student",
        )
        client = APIClient()
        url = reverse("accounts:login")
        resp = client.post(
            url,
            {"email": "loginok@example.com", "password": "StrongP@ssw0rd!"},
            format="json",
        )
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data["email"] == user.email
        assert "tokens" in resp.data and "access" in resp.data["tokens"] and "refresh" in resp.data["tokens"]

    def test_login_rejects_invalid_credentials(self):
        UserModel.objects.create_user(
            email="badpass@example.com",
            password="GoodPass123!",
            first_name="Bad",
            last_name="Cred",
            role="student",
        )
        client = APIClient()
        url = reverse("accounts:login")
        resp = client.post(
            url,
            {"email": "badpass@example.com", "password": "wrong"},
            format="json",
        )
        assert resp.status_code in (status.HTTP_401_UNAUTHORIZED, status.HTTP_400_BAD_REQUEST)
        # Our view returns 401 with {"detail": "Invalid credentials."}
        assert "detail" in resp.data

    def test_login_requires_email_and_password(self):
        client = APIClient()
        url = reverse("accounts:login")

        # Missing both
        resp = client.post(url, {}, format="json")
        assert resp.status_code == status.HTTP_400_BAD_REQUEST
        assert "email" in resp.data and "password" in resp.data

        # Missing password
        resp = client.post(url, {"email": "x@example.com"}, format="json")
        assert resp.status_code == status.HTTP_400_BAD_REQUEST
        assert "password" in resp.data

        # Missing email
        resp = client.post(url, {"password": "abc"}, format="json")
        assert resp.status_code == status.HTTP_400_BAD_REQUEST
        assert "email" in resp.data

    def test_login_email_normalization(self):
        UserModel.objects.create_user(
            email="normalize@example.com",
            password="StrongP@ssw0rd!",
            first_name="Norm",
            last_name="Alize",
            role="student",
        )
        client = APIClient()
        url = reverse("accounts:login")
        resp = client.post(
            url,
            {"email": "  NORMALIZE@EXAMPLE.COM  ", "password": "StrongP@ssw0rd!"},
            format="json",
        )
        assert resp.status_code == status.HTTP_200_OK

    def test_login_inactive_user_forbidden(self):
        user = UserModel.objects.create_user(
            email="inactive@example.com",
            password="StrongP@ssw0rd!",
            first_name="Ina",
            last_name="Ctive",
            role="student",
        )
        user.is_active = False
        user.save(update_fields=["is_active"])

        client = APIClient()
        url = reverse("accounts:login")
        resp = client.post(
            url,
            {"email": "inactive@example.com", "password": "StrongP@ssw0rd!"},
            format="json",
        )
        assert resp.status_code in (status.HTTP_403_FORBIDDEN, status.HTTP_401_UNAUTHORIZED)
