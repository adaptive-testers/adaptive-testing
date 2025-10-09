from __future__ import annotations

from typing import TYPE_CHECKING, Any

from django.contrib.auth import authenticate
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .serializers import UserRegistrationSerializer

if TYPE_CHECKING:
    from django.contrib.auth.models import AbstractBaseUser
    from django.http import HttpRequest
    from rest_framework.request import Request


class UserRegistrationView(generics.CreateAPIView):
    """
    User registration endpoint.
    POST /api/auth/register/
    """

    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request: Any, *args: Any, **kwargs: Any) -> Response:  # noqa: ARG002
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


@api_view(["POST"])  # type: ignore[misc]  # drf decorators are untyped for mypy
@permission_classes([AllowAny])  # type: ignore[misc]
def user_login_view(request: Request) -> Response:
    """
    User login endpoint.
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

    auth_user: AbstractBaseUser | None = authenticate(
        request, username=email, password=password
    )
    if not auth_user:
        return Response({"detail": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)
    if not auth_user.is_active:
        return Response({"detail": "User inactive."}, status=status.HTTP_403_FORBIDDEN)
    if not isinstance(auth_user, User):
        return Response({"detail": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)

    user = auth_user

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


@api_view(["GET", "PUT"])  # type: ignore[misc]
@permission_classes([IsAuthenticated])  # type: ignore[misc]
def user_profile_view(request: HttpRequest) -> Response:  # noqa: ARG001
    """
    User profile endpoint (stub).
    """
    return Response({"message": "Not implemented"}, status=status.HTTP_501_NOT_IMPLEMENTED)
