from django.contrib.auth import authenticate  # noqa: F401
from rest_framework import generics, status  # noqa: F401
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response  # noqa: F401
from rest_framework_simplejwt.tokens import RefreshToken  # noqa: F401

from .models import User

# from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer

# TODO: Create serializers.py file with these serializers:
# - UserRegistrationSerializer
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
    # serializer_class = UserSerializer # TODO: Create UserRegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        # TODO: Implement user registration logic
        # 1. Validate serializer
        # 2. Create user
        # 3. Generate JWT tokens
        # 4. Return user data + tokens
        pass


@api_view(["POST"])
@permission_classes([AllowAny])
def user_login_view(request): # noqa: ARG001
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
    pass


@api_view(["GET", "PUT"])
@permission_classes([IsAuthenticated])
def user_profile_view(request): # noqa: ARG001
    """
    User profile endpoint.

    GET /api/auth/profile/
    PUT /api/auth/profile/
    """
    # TODO: Implement user profile logic
    # GET: Return current user data
    # PUT: Update user profile
    pass


# TODO: Implement these endpoints:
# - User logout
# - User password change
# - User password reset
# - User email verification
# - User OAuth endpoints (Google, Microsoft)
