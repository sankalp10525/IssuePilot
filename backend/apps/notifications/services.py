"""
Notification services.
"""
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db import transaction
from django.utils import timezone

from apps.issues.models import Issue
from apps.notifications.models import Notification, OutboxMessage
from apps.projects.models import Project

User = get_user_model()


@transaction.atomic
def outbox_create(*, event_type: str, payload: dict) -> OutboxMessage:
    """Create an outbox message."""
    return OutboxMessage.objects.create(
        event_type=event_type,
        payload=payload,
    )


@transaction.atomic
def outbox_mark_processed(*, message: OutboxMessage) -> OutboxMessage:
    """Mark outbox message as processed."""
    message.status = OutboxMessage.Status.PROCESSED
    message.processed_at = timezone.now()
    message.save()
    return message


@transaction.atomic
def outbox_mark_failed(*, message: OutboxMessage, error: str) -> OutboxMessage:
    """Mark outbox message as failed."""
    message.status = OutboxMessage.Status.FAILED
    message.error_message = error
    message.retry_count += 1
    message.save()
    return message


@transaction.atomic
def notification_create(
    *,
    recipient: User,
    notification_type: str,
    title: str,
    message: str,
    project: Project = None,
    issue: Issue = None,
) -> Notification:
    """Create a notification."""
    return Notification.objects.create(
        recipient=recipient,
        notification_type=notification_type,
        title=title,
        message=message,
        project=project,
        issue=issue,
    )


@transaction.atomic
def notification_mark_read(*, notification: Notification) -> Notification:
    """Mark a notification as read."""
    if not notification.is_read:
        notification.is_read = True
        notification.read_at = timezone.now()
        notification.save()
    return notification


@transaction.atomic
def notification_mark_all_read(*, user: User) -> int:
    """Mark all notifications as read for a user."""
    return Notification.objects.filter(
        recipient=user,
        is_read=False
    ).update(is_read=True, read_at=timezone.now())


def notification_send_email(*, notification: Notification) -> None:
    """Send email notification."""
    # In production, use a proper email template
    send_mail(
        subject=notification.title,
        message=notification.message,
        from_email=None,  # Uses DEFAULT_FROM_EMAIL
        recipient_list=[notification.recipient.email],
        fail_silently=True,
    )


def process_outbox_message(*, message: OutboxMessage) -> None:
    """Process an outbox message and create notifications."""
    try:
        event_type = message.event_type
        payload = message.payload
        
        if event_type == "issue_assigned":
            _handle_issue_assigned(payload)
        elif event_type == "issue_commented":
            _handle_issue_commented(payload)
        elif event_type == "issue_state_changed":
            _handle_issue_state_changed(payload)
        # Add more event handlers as needed
        
        outbox_mark_processed(message=message)
    except Exception as e:
        outbox_mark_failed(message=message, error=str(e))


def _handle_issue_assigned(payload: dict) -> None:
    """Handle issue assignment notification."""
    try:
        issue = Issue.objects.get(id=payload["issue_id"])
        if issue.assignee:
            notification = notification_create(
                recipient=issue.assignee,
                notification_type=Notification.Type.ISSUE_ASSIGNED,
                title=f"You were assigned to {issue.key}",
                message=f"{issue.reporter.username} assigned you to {issue.title}",
                project=issue.project,
                issue=issue,
            )
            notification_send_email(notification=notification)
    except Issue.DoesNotExist:
        pass


def _handle_issue_commented(payload: dict) -> None:
    """Handle issue comment notification."""
    try:
        issue = Issue.objects.get(id=payload["issue_id"])
        author = User.objects.get(id=payload["author_id"])
        
        # Notify watchers (except the comment author)
        for watcher in issue.watchers.exclude(user=author):
            notification = notification_create(
                recipient=watcher.user,
                notification_type=Notification.Type.ISSUE_COMMENTED,
                title=f"New comment on {issue.key}",
                message=f"{author.username} commented on {issue.title}",
                project=issue.project,
                issue=issue,
            )
            notification_send_email(notification=notification)
    except (Issue.DoesNotExist, User.DoesNotExist):
        pass


def _handle_issue_state_changed(payload: dict) -> None:
    """Handle issue state change notification."""
    try:
        issue = Issue.objects.get(id=payload["issue_id"])
        actor = User.objects.get(id=payload["actor_id"])
        
        # Notify watchers (except the actor)
        for watcher in issue.watchers.exclude(user=actor):
            notification = notification_create(
                recipient=watcher.user,
                notification_type=Notification.Type.ISSUE_STATE_CHANGED,
                title=f"{issue.key} state changed",
                message=f"{actor.username} moved {issue.title} to {issue.state.name}",
                project=issue.project,
                issue=issue,
            )
    except (Issue.DoesNotExist, User.DoesNotExist):
        pass
