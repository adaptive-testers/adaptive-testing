import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

pytestmark = pytest.mark.django_db

def test_register_success_creates_user():
    client = APIClient()
    url = reverse("accounts:register")  # /api/auth/register/
    payload = {
        "email": "newuser@example.com",
        "password": "StrongP@ssw0rd!",
        "first_name": "New",
        "last_name": "User",
        "role": "student",   # valid choices: admin | instructor | student
    }
    resp = client.post(url, payload, format="json")
    assert resp.status_code in (status.HTTP_201_CREATED, status.HTTP_200_OK)

    User = get_user_model()
    assert User.objects.filter(email="newuser@example.com").exists()

def test_register_duplicate_email_returns_400():
    User = get_user_model()
    User.objects.create_user(
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
