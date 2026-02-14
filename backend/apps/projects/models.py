"""
Project models.
"""
from django.conf import settings
from django.db import models
from django.utils.text import slugify


class Project(models.Model):
    """Main project model."""
    
    name = models.CharField(max_length=255)
    key = models.CharField(max_length=10, unique=True, db_index=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="owned_projects"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "projects"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.key} - {self.name}"


class ProjectMembership(models.Model):
    """Project membership with roles."""
    
    class Role(models.TextChoices):
        OWNER = "owner", "Owner"
        ADMIN = "admin", "Admin"
        MEMBER = "member", "Member"
        VIEWER = "viewer", "Viewer"

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="memberships")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="project_memberships")
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.MEMBER)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "project_memberships"
        unique_together = [["project", "user"]]
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.user.username} - {self.project.key} ({self.role})"


class Board(models.Model):
    """Board for organizing issues (Kanban, Scrum, etc)."""
    
    class BoardType(models.TextChoices):
        KANBAN = "kanban", "Kanban"
        SCRUM = "scrum", "Scrum"

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="boards")
    name = models.CharField(max_length=255)
    board_type = models.CharField(max_length=20, choices=BoardType.choices, default=BoardType.KANBAN)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "boards"
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.project.key} - {self.name}"


class Sprint(models.Model):
    """Sprint for Scrum boards."""
    
    class Status(models.TextChoices):
        FUTURE = "future", "Future"
        ACTIVE = "active", "Active"
        CLOSED = "closed", "Closed"

    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name="sprints")
    name = models.CharField(max_length=255)
    goal = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.FUTURE)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "sprints"
        ordering = ["-start_date"]

    def __str__(self):
        return self.name


class Epic(models.Model):
    """Epic for grouping related issues."""
    
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="epics")
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    color = models.CharField(max_length=7, default="#6B7280")
    start_date = models.DateField(null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "epics"
        ordering = ["created_at"]

    def __str__(self):
        return self.name


class Workflow(models.Model):
    """Workflow definition for a project."""
    
    project = models.OneToOneField(Project, on_delete=models.CASCADE, related_name="workflow")
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "workflows"

    def __str__(self):
        return f"{self.project.key} - {self.name}"


class WorkflowState(models.Model):
    """State in a workflow."""
    
    class Category(models.TextChoices):
        TODO = "todo", "To Do"
        IN_PROGRESS = "in_progress", "In Progress"
        DONE = "done", "Done"

    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE, related_name="states")
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=Category.choices)
    order = models.PositiveIntegerField(default=0)
    is_initial = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "workflow_states"
        ordering = ["order"]
        unique_together = [["workflow", "name"]]

    def __str__(self):
        return f"{self.workflow.project.key} - {self.name}"


class WorkflowTransition(models.Model):
    """Allowed transition between workflow states."""
    
    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE, related_name="transitions")
    from_state = models.ForeignKey(
        WorkflowState,
        on_delete=models.CASCADE,
        related_name="transitions_from"
    )
    to_state = models.ForeignKey(
        WorkflowState,
        on_delete=models.CASCADE,
        related_name="transitions_to"
    )
    name = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "workflow_transitions"
        unique_together = [["workflow", "from_state", "to_state"]]

    def __str__(self):
        return f"{self.from_state.name} → {self.to_state.name}"
