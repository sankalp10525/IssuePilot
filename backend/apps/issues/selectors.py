"""
Issue selectors.
"""
from django.contrib.auth import get_user_model
from django.contrib.postgres.search import SearchQuery, SearchRank
from django.db.models import Prefetch, Q, QuerySet

from apps.issues.models import Attachment, Comment, Event, Issue, Watcher
from apps.projects.models import Project, Sprint

User = get_user_model()


def issue_list(*, project: Project, filters: dict = None) -> QuerySet:
    """Get issues for a project with optional filters."""
    qs = Issue.objects.filter(project=project).select_related(
        "project",
        "state",
        "reporter",
        "assignee",
        "sprint",
        "epic",
    ).prefetch_related("watchers__user")
    
    if not filters:
        return qs
    
    # Apply filters
    if "state" in filters:
        qs = qs.filter(state_id=filters["state"])
    if "assignee" in filters:
        qs = qs.filter(assignee_id=filters["assignee"])
    if "reporter" in filters:
        qs = qs.filter(reporter_id=filters["reporter"])
    if "sprint" in filters:
        qs = qs.filter(sprint_id=filters["sprint"])
    if "epic" in filters:
        qs = qs.filter(epic_id=filters["epic"])
    if "issue_type" in filters:
        qs = qs.filter(issue_type=filters["issue_type"])
    if "priority" in filters:
        qs = qs.filter(priority=filters["priority"])
    
    return qs


def issue_search(*, project: Project, query: str) -> QuerySet:
    """Full-text search for issues."""
    search_query = SearchQuery(query)
    return Issue.objects.filter(
        project=project
    ).filter(
        Q(search_vector=search_query) | Q(key__icontains=query) | Q(title__icontains=query)
    ).annotate(
        rank=SearchRank("search_vector", search_query)
    ).order_by("-rank", "-created_at")


def issue_get_by_id(*, issue_id: int) -> Issue:
    """Get issue by ID."""
    return Issue.objects.select_related(
        "project",
        "state",
        "reporter",
        "assignee",
        "sprint",
        "epic",
        "parent",
    ).prefetch_related(
        "watchers__user",
        "attachments",
        "subtasks",
    ).get(id=issue_id)


def issue_get_by_key(*, key: str) -> Issue:
    """Get issue by key."""
    return Issue.objects.select_related(
        "project",
        "state",
        "reporter",
        "assignee",
        "sprint",
        "epic",
        "parent",
    ).prefetch_related(
        "watchers__user",
        "attachments",
        "subtasks",
    ).get(key=key)


def comment_list(*, issue: Issue) -> QuerySet:
    """Get comments for an issue."""
    return Comment.objects.filter(issue=issue).select_related("author")


def attachment_list(*, issue: Issue) -> QuerySet:
    """Get attachments for an issue."""
    return Attachment.objects.filter(issue=issue).select_related("uploaded_by")


def watcher_list(*, issue: Issue) -> QuerySet:
    """Get watchers for an issue."""
    return Watcher.objects.filter(issue=issue).select_related("user")


def is_watching(*, issue: Issue, user: User) -> bool:
    """Check if user is watching an issue."""
    return Watcher.objects.filter(issue=issue, user=user).exists()


def event_list_by_project(*, project: Project, limit: int = 50) -> QuerySet:
    """Get recent events for a project."""
    return Event.objects.filter(project=project).select_related(
        "actor", "issue"
    )[:limit]


def event_list_by_issue(*, issue: Issue) -> QuerySet:
    """Get events for an issue."""
    return Event.objects.filter(issue=issue).select_related("actor")
