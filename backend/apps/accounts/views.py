from typing import Any

from django.contrib.auth import authenticate  # noqa: F401
from django.http import HttpRequest
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
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
# - UserLoginSerializer
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
def user_login_view(request: HttpRequest) -> Response: # noqa: ARG001
    """
    User login endpoint.

    POST /api/auth/login/
    Body: {
        "email": "user@example.com",
        "password": "securepassword"
    }
    """
    # TODO: Implement user login logic
    # 1. Validate credentials
    # 2. Generate JWT tokens
    # 3. Return user data + tokens
    return Response({"message": "Not implemented"}, status=status.HTTP_501_NOT_IMPLEMENTED)


@api_view(["GET", "PUT"])
@permission_classes([IsAuthenticated])
def user_profile_view(request: HttpRequest) -> Response: # noqa: ARG001
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
# - User logout done?
# - User password change
# - User password reset
# - User email verification
# - User OAuth endpoints (Google, Microsoft)

@api_view["POST"]
@permission_classes([IsAuthenticated])
def user_logout_view(request):
    """
    User logout endpoint.

    POST /api/auth/logout/
    Body: {
        "refresh": "<refresh_token>"
    }

    """
    try:
        refresh_token = request.data["refresh"]
        token = RefreshToken(refresh_token)
        token.blacklist()  # mark token as invalid
        return Response({"message": "Successfully logged out."}, status=status.HTTP_205_RESET_CONTENT)
    except KeyError:
        return Response({"error": "Refresh token required."}, status=status.HTTP_400_BAD_REQUEST)
    except TokenError:
        return Response({"error": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)
