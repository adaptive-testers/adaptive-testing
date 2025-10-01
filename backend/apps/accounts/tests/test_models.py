import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model

pytestmark = pytest.mark.django_db

def test_register_returns_tokens_on_success():
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

def test_register_rejects_weak_password():
    client = APIClient()
    url = reverse("accounts:register")
    payload = {
        "email": "weakpass@example.com",
        "password": "123",  # should trip password validators
        "first_name": "Weak",
        "last_name": "Pass",
        "role": "student",
    }
    resp = client.post(url, payload, format="json")
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    assert "password" in resp.data

def test_register_rejects_invalid_role():
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

def test_register_missing_required_fields():
    client = APIClient()
    url = reverse("accounts:register")
    resp = client.post(url, {}, format="json")
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    # Adjust if your serializer marks some fields optional
    for field in ("email", "first_name", "last_name", "password"):
        assert field in resp.data

def test_register_email_normalized_lowercase():
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

    User = get_user_model()
    assert User.objects.filter(email="newuser@example.com").exists()
