from typing import Any, cast

from django.contrib.auth import authenticate  # noqa: F401
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .serializers import (  # noqa: F401
    UserLoginSerializer,
    UserProfileSerializer,
    UserRegistrationSerializer,
)

# TODO: Create serializers.py file with these serializers:
# - UserRegistrationSerializer DONE
# - UserLoginSerializer DONE
# - UserProfileSerializer


class UserRegistrationView(generics.CreateAPIView):
    """
    User registration endpoint.

    POST /api/auth/register/
    Body: {
        "email": "user@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "password": "securepassword",
        "role": "student" # or "instructor" or "admin"
    }
    """

    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request: Any) -> Response:
        # TODO: Implement user registration logic
        # 1. Validate serializer
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 2. Create user
        user = serializer.save()

        # 3. Generate JWT tokens
        refresh = RefreshToken.for_user(user)

        # 4. Return user data + tokens
        data = serializer.data
        data["tokens"] = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

        return Response(data, status=status.HTTP_201_CREATED)


@api_view(["POST"])
@permission_classes([AllowAny])
def user_login_view(request: Request) -> Response:
    """
    User login endpoint.

    POST /api/auth/login/
    Body: {
        "email": "user@example.com",
        "password": "securepassword"
    }
    """
    serializer = UserLoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data["email"].strip().lower()
    password = serializer.validated_data["password"]
    authed = authenticate(request, username=email, password=password)
    if not authed:
        return Response({"detail": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)

    if not authed.is_active:
        return Response({"detail": "User inactive."}, status=status.HTTP_403_FORBIDDEN)

    user = authed
    refresh = RefreshToken.for_user(user)
    data = {
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "role": user.role,
        "tokens": {"refresh": str(refresh), "access": str(refresh.access_token)},
    }

    return Response(data, status=status.HTTP_200_OK)


@api_view(["GET", "PUT"])
@permission_classes([IsAuthenticated])
def user_profile_view(request: Request) -> Response:
    """
    User profile endpoint.

    GET /api/auth/profile/
    PUT /api/auth/profile/
    """
    # TODO: Implement user profile logic
    # GET: Return current user data
    # PUT: Update user profile
    return Response({"message": "Not implemented"}, status=status.HTTP_501_NOT_IMPLEMENTED)

# TODO: Implement these endpoints:
# - User logout
# - User password change
# - User password reset
# - User email verification
# - User OAuth endpoints (Google, Microsoft)
