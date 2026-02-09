"""
Issue models.
"""
from django.conf import settings
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField
from django.db import models

from apps.projects.models import Epic, Project, Sprint, WorkflowState


class Issue(models.Model):
    """Main issue model."""
    
    class Type(models.TextChoices):
        TASK = "task", "Task"
        BUG = "bug", "Bug"
        STORY = "story", "Story"
        EPIC = "epic", "Epic"

    class Priority(models.TextChoices):
        LOWEST = "lowest", "Lowest"
        LOW = "low", "Low"
        MEDIUM = "medium", "Medium"
        HIGH = "high", "High"
        HIGHEST = "highest", "Highest"

    # Identifiers
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="issues")
    key = models.CharField(max_length=50, unique=True, db_index=True)  # e.g., PROJ-123
    sequence = models.PositiveIntegerField()  # Auto-increment per project

    # Content
    title = models.CharField(max_length=500)
    description = models.TextField(blank=True)
    issue_type = models.CharField(max_length=20, choices=Type.choices, default=Type.TASK)
    priority = models.CharField(max_length=20, choices=Priority.choices, default=Priority.MEDIUM)

    # Relationships
    state = models.ForeignKey(WorkflowState, on_delete=models.PROTECT, related_name="issues")
    sprint = models.ForeignKey(Sprint, on_delete=models.SET_NULL, null=True, blank=True, related_name="issues")
    epic = models.ForeignKey(Epic, on_delete=models.SET_NULL, null=True, blank=True, related_name="issues")
    parent = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True, related_name="subtasks")

    # People
    reporter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="reported_issues"
    )
    assignee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_issues"
    )

    # Estimates
    story_points = models.PositiveIntegerField(null=True, blank=True)
    time_estimate = models.PositiveIntegerField(null=True, blank=True, help_text="Estimate in minutes")
    time_spent = models.PositiveIntegerField(default=0, help_text="Time spent in minutes")

    # Dates
    due_date = models.DateField(null=True, blank=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Full-text search
    search_vector = SearchVectorField(null=True, blank=True)

    class Meta:
        db_table = "issues"
        ordering = ["-created_at"]
        unique_together = [["project", "sequence"]]
        indexes = [
            models.Index(fields=["project", "state"]),
            models.Index(fields=["assignee"]),
            models.Index(fields=["sprint"]),
            GinIndex(fields=["search_vector"]),
        ]

    def __str__(self):
        return f"{self.key} - {self.title}"

    def save(self, *args, **kwargs):
        if not self.sequence:
            # Auto-increment sequence per project
            last_issue = Issue.objects.filter(project=self.project).order_by("-sequence").first()
            self.sequence = (last_issue.sequence + 1) if last_issue else 1
        
        if not self.key:
            self.key = f"{self.project.key}-{self.sequence}"
        
        super().save(*args, **kwargs)


class Comment(models.Model):
    """Comment on an issue."""
    
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "comments"
        ordering = ["created_at"]

    def __str__(self):
        return f"Comment by {self.author.username} on {self.issue.key}"


class Attachment(models.Model):
    """File attachment for an issue."""
    
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name="attachments")
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="attachments")
    file = models.FileField(upload_to="attachments/%Y/%m/%d/")
    filename = models.CharField(max_length=255)
    file_size = models.PositiveIntegerField()  # bytes
    content_type = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "attachments"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.filename} on {self.issue.key}"


class Watcher(models.Model):
    """User watching an issue for updates."""
    
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name="watchers")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="watched_issues")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "watchers"
        unique_together = [["issue", "user"]]
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.user.username} watching {self.issue.key}"


class Event(models.Model):
    """Event tracking for activity feed."""
    
    class EventType(models.TextChoices):
        ISSUE_CREATED = "issue_created", "Issue Created"
        ISSUE_UPDATED = "issue_updated", "Issue Updated"
        ISSUE_DELETED = "issue_deleted", "Issue Deleted"
        STATE_CHANGED = "state_changed", "State Changed"
        COMMENT_ADDED = "comment_added", "Comment Added"
        ATTACHMENT_ADDED = "attachment_added", "Attachment Added"
        ASSIGNEE_CHANGED = "assignee_changed", "Assignee Changed"
        SPRINT_CHANGED = "sprint_changed", "Sprint Changed"

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="events")
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, null=True, blank=True, related_name="events")
    event_type = models.CharField(max_length=50, choices=EventType.choices)
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="events")
    data = models.JSONField(default=dict, blank=True)  # Additional event data
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "events"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["project", "-created_at"]),
            models.Index(fields=["issue", "-created_at"]),
        ]

    def __str__(self):
        return f"{self.event_type} by {self.actor} at {self.created_at}"
