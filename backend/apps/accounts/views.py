from typing import Any

from django.contrib.auth import authenticate
from django.http import HttpRequest
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .serializers import UserRegistrationSerializer

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

    # match DRF CreateModelMixin.create signature
    def create(self, request: Any, *_: Any, **__: Any) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        refresh = RefreshToken.for_user(user)
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
    Body:
    {
        "email": "user@example.com",
        "password": "securepassword"
    }

    Response (200):
    {
        "email": "...",
        "first_name": "...",
        "last_name": "...",
        "role": "...",
        "tokens": {
            "refresh": "...",
            "access": "..."
        }
    }
    """
    email_raw = request.data.get("email")
    password = request.data.get("password")

    errors: dict[str, list[str]] = {}
    if not email_raw:
        errors.setdefault("email", []).append("This field is required.")
    if not password:
        errors.setdefault("password", []).append("This field is required.")
    if errors:
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)

    email = str(email_raw).strip().lower()

    user = authenticate(request, username=email, password=password)
    if not user:
        return Response({"detail": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)

    if not user.is_active:
        return Response({"detail": "User inactive."}, status=status.HTTP_403_FORBIDDEN)

    refresh = RefreshToken.for_user(user)
    data = {
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "role": user.role,
        "tokens": {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        },
    }
    return Response(data, status=status.HTTP_200_OK)


@api_view(["GET", "PUT"])
@permission_classes([IsAuthenticated])
def user_profile_view(_request: HttpRequest) -> Response:
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
