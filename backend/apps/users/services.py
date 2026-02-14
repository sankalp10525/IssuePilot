"""
User services (business logic).
"""
from django.contrib.auth import get_user_model
from django.db import transaction

User = get_user_model()


@transaction.atomic
def user_create(
    *,
    username: str,
    email: str,
    password: str,
    first_name: str = "",
    last_name: str = "",
    **kwargs
) -> User:
    """Create a new user."""
    user = User.objects.create_user(
        username=username,
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name,
        **kwargs
    )
    return user


@transaction.atomic
def user_update(*, user: User, **data) -> User:
    """Update user fields."""
    for field, value in data.items():
        if field == "password":
            user.set_password(value)
        else:
            setattr(user, field, value)
    user.save()
    return user


@transaction.atomic
def user_delete(*, user: User) -> None:
    """Delete a user."""
    user.delete()
