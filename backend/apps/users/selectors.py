"""
User selectors (read queries).
"""
from django.contrib.auth import get_user_model
from django.db.models import QuerySet

User = get_user_model()


def user_list() -> QuerySet:
    """Return all users."""
    return User.objects.all()


def user_get_by_id(user_id: int) -> User:
    """Get user by ID."""
    return User.objects.get(id=user_id)


def user_get_by_username(username: str) -> User:
    """Get user by username."""
    return User.objects.get(username=username)


def user_get_by_email(email: str) -> User:
    """Get user by email."""
    return User.objects.get(email=email)


def user_search(query: str) -> QuerySet:
    """Search users by username, email, or name."""
    return User.objects.filter(
        models.Q(username__icontains=query)
        | models.Q(email__icontains=query)
        | models.Q(first_name__icontains=query)
        | models.Q(last_name__icontains=query)
    )
