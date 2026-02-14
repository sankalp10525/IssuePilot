"""
Notification models with Outbox pattern.
"""
from django.conf import settings
from django.db import models

from apps.issues.models import Issue
from apps.projects.models import Project


class OutboxMessage(models.Model):
    """Outbox for reliable message processing."""
    
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        PROCESSING = "processing", "Processing"
        PROCESSED = "processed", "Processed"
        FAILED = "failed", "Failed"

    event_type = models.CharField(max_length=50)
    payload = models.JSONField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    error_message = models.TextField(blank=True)
    retry_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "outbox_messages"
        ordering = ["created_at"]
        indexes = [
            models.Index(fields=["status", "created_at"]),
        ]

    def __str__(self):
        return f"{self.event_type} - {self.status}"


class Notification(models.Model):
    """User notification."""
    
    class Type(models.TextChoices):
        ISSUE_ASSIGNED = "issue_assigned", "Issue Assigned"
        ISSUE_MENTIONED = "issue_mentioned", "Issue Mentioned"
        ISSUE_COMMENTED = "issue_commented", "Issue Commented"
        ISSUE_STATE_CHANGED = "issue_state_changed", "Issue State Changed"
        PROJECT_INVITED = "project_invited", "Project Invited"

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications"
    )
    notification_type = models.CharField(max_length=50, choices=Type.choices)
    title = models.CharField(max_length=255)
    message = models.TextField()
    
    # Links
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, null=True, blank=True)
    
    # Status
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "notifications"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["recipient", "is_read", "-created_at"]),
        ]

    def __str__(self):
        return f"{self.title} for {self.recipient.username}"
