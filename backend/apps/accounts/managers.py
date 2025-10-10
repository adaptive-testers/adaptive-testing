from __future__ import annotations

from typing import TYPE_CHECKING, Any, cast, overload

from django.contrib.auth.models import UserManager as DjangoUserManager

if TYPE_CHECKING:
    from .models import User


class UserManager(DjangoUserManager["User"]):
    """Custom user manager supporting both Django's (username, email, password)
    and our email-only invocation.
    """

    # --- Overloads: callers can use either form ---

    # kwargs-only: create_user(email=..., password=..., **extra)
    @overload
    def create_user(self, *, email: str, password: str | None = ..., **extra_fields: Any) -> User: ...
    # Django-form: create_user(username, email=None, password=None, **extra)
    @overload
    def create_user(self, username: str, email: str | None = ..., password: str | None = ..., **extra_fields: Any) -> User: ...

    def create_user(self, *args: Any, **kwargs: Any) -> User:
        """
        Implementation accepts both overload shapes:
          - create_user(email=..., password=..., **extra)
          - create_user(username, email=None, password=None, **extra)
        """
        # Normalize inputs
        email: str | None = kwargs.pop("email", None)
        password: str | None = kwargs.pop("password", None)

        # If called with positional Django signature, map them
        # args: (username, [email], [password], ...)
        if email is None and len(args) >= 2:
            email = args[1]
        if password is None and len(args) >= 3:
            password = args[2]

        if not email:
            raise ValueError("The Email field must be set")

        email = self.normalize_email(email)
        user = cast("User", self.model(email=email, **kwargs))
        user.set_password(password)
        user.save(using=self._db)
        return user

    # Overloads for superuser
    @overload
    def create_superuser(self, *, email: str, password: str | None = ..., **extra_fields: Any) -> User: ...
    @overload
    def create_superuser(self, username: str, email: str | None = ..., password: str | None = ..., **extra_fields: Any) -> User: ...

    def create_superuser(self, *args: Any, **kwargs: Any) -> User:
        """
        Implementation accepts both overload shapes; enforces superuser flags.
        """
        kwargs.setdefault("is_staff", True)
        kwargs.setdefault("is_superuser", True)
        kwargs.setdefault("is_active", True)

        if kwargs.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if kwargs.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        # Pull normalized email/password the same way
        email: str | None = kwargs.get("email")
        password: str | None = kwargs.get("password")

        if email is None and len(args) >= 2:
            email = args[1]
        if password is None and len(args) >= 3:
            password = args[2]

        # Call our create_user using kwargs form to avoid the username/None issue
        if email is None:
            raise ValueError("The Email field must be set")
        return self.create_user(email=email, password=password, **kwargs)
