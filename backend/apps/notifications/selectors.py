"""
Notification selectors.
"""
from django.contrib.auth import get_user_model
from django.db.models import QuerySet

from apps.notifications.models import Notification, OutboxMessage

User = get_user_model()


def notification_list(*, user: User, is_read: bool = None) -> QuerySet:
    """Get notifications for a user."""
    qs = Notification.objects.filter(recipient=user).select_related("project", "issue")
    
    if is_read is not None:
        qs = qs.filter(is_read=is_read)
    
    return qs


def notification_unread_count(*, user: User) -> int:
    """Count unread notifications for a user."""
    return Notification.objects.filter(recipient=user, is_read=False).count()


def outbox_pending_messages(*, limit: int = 100) -> QuerySet:
    """Get pending outbox messages."""
    return OutboxMessage.objects.filter(
        status=OutboxMessage.Status.PENDING
    ).order_by("created_at")[:limit]
