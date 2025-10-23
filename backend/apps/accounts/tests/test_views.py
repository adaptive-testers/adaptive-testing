from typing import TYPE_CHECKING, cast

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

if TYPE_CHECKING:
    from apps.accounts.models import User

UserModel = cast("type[User]", get_user_model())

pytestmark = pytest.mark.django_db


# =========================
# Registration View Tests
# =========================
class TestUserRegistrationView:
    def test_register_success_creates_user(self):
        client = APIClient()
        url = reverse("accounts:register")
        payload = {
            "email": "newuser@example.com",
            "password": "StrongP@ssw0rd!",
            "first_name": "New",
            "last_name": "User",
            "role": "student",  # valid: admin | instructor | student
        }
        resp = client.post(url, payload, format="json")
        assert resp.status_code in (status.HTTP_201_CREATED, status.HTTP_200_OK)

        assert UserModel.objects.filter(email="newuser@example.com").exists()

    def test_register_duplicate_email_returns_400(self):
        UserModel.objects.create_user(
            email="taken@example.com",
            password="abc12345",
            first_name="T",
            last_name="A",
            role="student",
        )

        client = APIClient()
        url = reverse("accounts:register")
        payload = {
            "email": "taken@example.com",
            "password": "Another$trong123",
            "first_name": "New",
            "last_name": "User",
            "role": "student",
        }
        resp = client.post(url, payload, format="json")
        assert resp.status_code == status.HTTP_400_BAD_REQUEST

    def test_register_returns_tokens_on_success(self):
        client = APIClient()
        url = reverse("accounts:register")
        payload = {
            "email": "tokentest@example.com",
            "password": "StrongP@ssw0rd!",
            "first_name": "Tok",
            "last_name": "En",
            "role": "student",
        }
        resp = client.post(url, payload, format="json")
        assert resp.status_code in (status.HTTP_201_CREATED, status.HTTP_200_OK)
        assert "tokens" in resp.data
        assert "access" in resp.data["tokens"]
        assert "refresh" in resp.data["tokens"]

    def test_register_rejects_weak_password(self):
        client = APIClient()
        url = reverse("accounts:register")
        payload = {
            "email": "weakpass@example.com",
            "password": "123",  # rejected by validators
            "first_name": "Weak",
            "last_name": "Pass",
            "role": "student",
        }
        resp = client.post(url, payload, format="json")
        assert resp.status_code == status.HTTP_400_BAD_REQUEST
        assert "password" in resp.data

    def test_register_rejects_invalid_role(self):
        client = APIClient()
        url = reverse("accounts:register")
        payload = {
            "email": "badrole@example.com",
            "password": "StrongP@ssw0rd!",
            "first_name": "Bad",
            "last_name": "Role",
            "role": "not_a_role",
        }
        resp = client.post(url, payload, format="json")
        assert resp.status_code == status.HTTP_400_BAD_REQUEST
        assert "role" in resp.data

    def test_register_missing_required_fields(self):
        client = APIClient()
        url = reverse("accounts:register")
        resp = client.post(url, {}, format="json")
        assert resp.status_code == status.HTTP_400_BAD_REQUEST
        for field in ("email", "first_name", "last_name", "password"):
            assert field in resp.data

    def test_register_email_normalized_lowercase(self):
        client = APIClient()
        url = reverse("accounts:register")
        payload = {
            "email": "  NEWUSER@EXAMPLE.COM ",
            "password": "StrongP@ssw0rd!",
            "first_name": "New",
            "last_name": "User",
            "role": "student",
        }
        resp = client.post(url, payload, format="json")
        assert resp.status_code in (status.HTTP_201_CREATED, status.HTTP_200_OK)

        assert UserModel.objects.filter(email="newuser@example.com").exists()

    def test_register_invalid_email_format(self):
        client = APIClient()
        url = reverse("accounts:register")
        payload = {
            "email": "not-an-email",
            "password": "StrongP@ssw0rd!",
            "first_name": "Bad",
            "last_name": "Email",
            "role": "student",
        }
        resp = client.post(url, payload, format="json")
        assert resp.status_code == status.HTTP_400_BAD_REQUEST
        assert "email" in resp.data


# =========================
# Login View Tests (8)
# =========================
class TestUserLoginView:
    # ---------- SUCCESS (4) ----------
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
        assert "tokens" in resp.data
        assert "access" in resp.data["tokens"]
        assert "refresh" in resp.data["tokens"]

    def test_login_success_with_email_normalization_spaces_and_case(self):
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
            {"email": "   NORMALIZE@EXAMPLE.COM   ", "password": "StrongP@ssw0rd!"},
            format="json",
        )
        assert resp.status_code == status.HTTP_200_OK

    def test_login_success_case_insensitive_email(self):
        UserModel.objects.create_user(
            email="mixcase@example.com",
            password="StrongP@ssw0rd!",
            first_name="Mix",
            last_name="Case",
            role="instructor",
        )
        client = APIClient()
        url = reverse("accounts:login")
        resp = client.post(
            url,
            {"email": "MixCase@Example.com", "password": "StrongP@ssw0rd!"},
            format="json",
        )
        assert resp.status_code == status.HTTP_200_OK
        for k in ("email", "first_name", "last_name", "role", "tokens"):
            assert k in resp.data

    def test_login_success_returns_expected_token_fields(self):
        UserModel.objects.create_user(
            email="tokencheck@example.com",
            password="StrongP@ssw0rd!",
            first_name="Tok",
            last_name="Check",
            role="admin",
        )
        client = APIClient()
        url = reverse("accounts:login")
        resp = client.post(
            url,
            {"email": "tokencheck@example.com", "password": "StrongP@ssw0rd!"},
            format="json",
        )
        assert resp.status_code == status.HTTP_200_OK
        assert set(resp.data["tokens"].keys()) == {"access", "refresh"}

    # ---------- FAILURE (4) ----------
    def test_login_rejects_invalid_password(self):
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
        assert "detail" in resp.data  # "Invalid credentials."

    def test_login_missing_both_fields(self):
        client = APIClient()
        url = reverse("accounts:login")
        resp = client.post(url, {}, format="json")
        assert resp.status_code == status.HTTP_400_BAD_REQUEST
        assert "email" in resp.data and "password" in resp.data

    def test_login_missing_email_only(self):
        client = APIClient()
        url = reverse("accounts:login")
        resp = client.post(url, {"password": "whatever"}, format="json")
        assert resp.status_code == status.HTTP_400_BAD_REQUEST
        assert "email" in resp.data

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


# =========================
# Profile View Tests
# =========================
class TestUserProfileView:
    """Test user profile endpoint functionality."""

    def test_get_profile_success(self):
        """Test that authenticated user can retrieve their profile."""
        user = UserModel.objects.create_user(
            email="profile@example.com",
            password="StrongP@ssw0rd!",
            first_name="Profile",
            last_name="User",
            role="student",
        )

        client = APIClient()
        client.force_authenticate(user=user)
        url = reverse("accounts:profile")
        response = client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["email"] == user.email
        assert response.data["first_name"] == user.first_name
        assert response.data["last_name"] == user.last_name
        assert response.data["role"] == user.role
        assert "created_at" in response.data

    def test_get_profile_unauthorized(self):
        """Test that unauthenticated user cannot access profile."""
        client = APIClient()
        url = reverse("accounts:profile")
        response = client.get(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_patch_profile_success(self):
        """Test that user can update their profile."""
        user = UserModel.objects.create_user(
            email="update@example.com",
            password="StrongP@ssw0rd!",
            first_name="Original",
            last_name="Name",
            role="student",
        )

        client = APIClient()
        client.force_authenticate(user=user)
        url = reverse("accounts:profile")
        update_data = {
            "first_name": "Updated",
            "last_name": "Name",
        }
        response = client.patch(url, update_data, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["first_name"] == "Updated"
        assert response.data["last_name"] == "Name"
        
        # Verify the user was actually updated
        user.refresh_from_db()
        assert user.first_name == "Updated"
        assert user.last_name == "Name"

    def test_patch_profile_validation_errors(self):
        """Test that profile update validates input properly."""
        user = UserModel.objects.create_user(
            email="validation@example.com",
            password="StrongP@ssw0rd!",
            first_name="Test",
            last_name="User",
            role="student",
        )

        client = APIClient()
        client.force_authenticate(user=user)
        url = reverse("accounts:profile")
        
        # Test empty first name
        update_data = {"first_name": "   "}
        response = client.patch(url, update_data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "first_name" in response.data

        # Test empty last name
        update_data = {"last_name": ""}
        response = client.patch(url, update_data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "last_name" in response.data

    def test_patch_profile_readonly_fields(self):
        """Test that readonly fields cannot be updated."""
        user = UserModel.objects.create_user(
            email="readonly@example.com",
            password="StrongP@ssw0rd!",
            first_name="Test",
            last_name="User",
            role="student",
        )

        client = APIClient()
        client.force_authenticate(user=user)
        url = reverse("accounts:profile")
        
        # Try to update readonly fields
        update_data = {
            "email": "hacker@example.com",
            "role": "admin",
            "created_at": "2020-01-01T00:00:00Z",
        }
        response = client.patch(url, update_data, format="json")

        # Should succeed but readonly fields should be ignored
        assert response.status_code == status.HTTP_200_OK
        assert response.data["email"] == user.email  # Should remain unchanged
        assert response.data["role"] == user.role     # Should remain unchanged

    def test_patch_profile_unauthorized(self):
        """Test that unauthenticated user cannot update profile."""
        client = APIClient()
        url = reverse("accounts:profile")
        update_data = {"first_name": "Hacker"}
        response = client.patch(url, update_data, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_patch_profile_partial_update(self):
        """Test that partial updates work correctly."""
        user = UserModel.objects.create_user(
            email="partial@example.com",
            password="StrongP@ssw0rd!",
            first_name="Original",
            last_name="Name",
            role="student",
        )

        client = APIClient()
        client.force_authenticate(user=user)
        url = reverse("accounts:profile")
        
        # Update only first name
        update_data = {"first_name": "Updated"}
        response = client.patch(url, update_data, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["first_name"] == "Updated"
        assert response.data["last_name"] == "Name"  # Should remain unchanged
        
        # Verify the user was actually updated
        user.refresh_from_db()
        assert user.first_name == "Updated"
        assert user.last_name == "Name"  # Should remain unchanged
