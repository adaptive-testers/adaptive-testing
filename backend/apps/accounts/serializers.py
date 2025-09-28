from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.

    TODO: Implement this serializer with:
    - Email validation
    - Password confirmation
    - Role validation
    """

    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "email",
            "first_name",
            "last_name",
            "password",
            "password_confirm",
            "role",
        ]

    # TODO: Add validation methods


class UserLoginSerializer(serializers.ModelSerializer):
    """
    Serializer for user login.

    TODO: Implement this serializer with:
    - Email validation
    - Password validation
    """

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["email", "password"]

    # TODO: Add validation methods


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for user profile.

    TODO: Implement this serializer with:
    - Read-only fields
    - Update validation
    """

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

    # TODO: Add validation methods
