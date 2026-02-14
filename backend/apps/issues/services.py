"""
Issue services.
"""
from django.contrib.auth import get_user_model
from django.contrib.postgres.search import SearchVector
from django.db import transaction
from django.utils import timezone

from apps.issues.models import Attachment, Comment, Event, Issue, Watcher
from apps.projects.models import Epic, Project, Sprint, WorkflowState
from apps.projects.selectors import workflow_can_transition

User = get_user_model()


@transaction.atomic
def issue_create(
    *,
    project: Project,
    title: str,
    reporter: User,
    description: str = "",
    issue_type: str = Issue.Type.TASK,
    priority: str = Issue.Priority.MEDIUM,
    assignee: User = None,
    sprint: Sprint = None,
    epic: Epic = None,
    parent: Issue = None,
    **kwargs
) -> Issue:
    """Create a new issue."""
    from apps.projects.selectors import workflow_get_initial_state
    
    # Get initial state from workflow
    initial_state = workflow_get_initial_state(workflow=project.workflow)
    
    issue = Issue.objects.create(
        project=project,
        title=title,
        description=description,
        issue_type=issue_type,
        priority=priority,
        state=initial_state,
        reporter=reporter,
        assignee=assignee,
        sprint=sprint,
        epic=epic,
        parent=parent,
        **kwargs
    )
    
    # Update search vector
    issue.search_vector = SearchVector("title", weight="A") + SearchVector("description", weight="B")
    issue.save(update_fields=["search_vector"])
    
    # Create event
    event_create(
        project=project,
        issue=issue,
        event_type=Event.EventType.ISSUE_CREATED,
        actor=reporter,
        data={"title": title, "key": issue.key},
    )
    
    # Auto-watch for reporter
    watcher_add(issue=issue, user=reporter)
    
    return issue


@transaction.atomic
def issue_update(*, issue: Issue, actor: User, **data) -> Issue:
    """Update an issue."""
    old_values = {}
    
    # Track changes for events
    if "assignee" in data and data["assignee"] != issue.assignee:
        old_values["assignee"] = issue.assignee
        issue.assignee = data.pop("assignee")
        if issue.assignee:
            watcher_add(issue=issue, user=issue.assignee)
    
    if "sprint" in data and data["sprint"] != issue.sprint:
        old_values["sprint"] = issue.sprint
        issue.sprint = data.pop("sprint")
    
    if "state" in data and data["state"] != issue.state:
        old_values["state"] = issue.state
        new_state = data.pop("state")
        # Validate transition
        if not workflow_can_transition(from_state=issue.state, to_state=new_state):
            raise ValueError(f"Invalid transition from {issue.state.name} to {new_state.name}")
        issue.state = new_state
        
        # Mark as resolved if moving to done category
        if new_state.category == "done" and not issue.resolved_at:
            issue.resolved_at = timezone.now()
        elif new_state.category != "done" and issue.resolved_at:
            issue.resolved_at = None
    
    # Update other fields
    for field, value in data.items():
        setattr(issue, field, value)
    
    # Update search vector if title or description changed
    if "title" in data or "description" in data:
        issue.search_vector = SearchVector("title", weight="A") + SearchVector("description", weight="B")
    
    issue.save()
    
    # Create update event
    event_create(
        project=issue.project,
        issue=issue,
        event_type=Event.EventType.ISSUE_UPDATED,
        actor=actor,
        data={"changes": old_values, "key": issue.key},
    )
    
    return issue


@transaction.atomic
def issue_transition(*, issue: Issue, to_state: WorkflowState, actor: User) -> Issue:
    """Transition issue to a new state."""
    if not workflow_can_transition(from_state=issue.state, to_state=to_state):
        raise ValueError(f"Invalid transition from {issue.state.name} to {to_state.name}")
    
    old_state = issue.state
    issue.state = to_state
    
    # Mark as resolved if moving to done category
    if to_state.category == "done" and not issue.resolved_at:
        issue.resolved_at = timezone.now()
    elif to_state.category != "done" and issue.resolved_at:
        issue.resolved_at = None
    
    issue.save()
    
    # Create state change event
    event_create(
        project=issue.project,
        issue=issue,
        event_type=Event.EventType.STATE_CHANGED,
        actor=actor,
        data={
            "key": issue.key,
            "from_state": old_state.name,
            "to_state": to_state.name,
        },
    )
    
    return issue


@transaction.atomic
def issue_delete(*, issue: Issue, actor: User) -> None:
    """Delete an issue."""
    # Create deletion event first
    event_create(
        project=issue.project,
        issue=None,
        event_type=Event.EventType.ISSUE_DELETED,
        actor=actor,
        data={"key": issue.key, "title": issue.title},
    )
    
    issue.delete()


@transaction.atomic
def comment_create(*, issue: Issue, author: User, content: str) -> Comment:
    """Create a comment on an issue."""
    comment = Comment.objects.create(
        issue=issue,
        author=author,
        content=content,
    )
    
    # Create event
    event_create(
        project=issue.project,
        issue=issue,
        event_type=Event.EventType.COMMENT_ADDED,
        actor=author,
        data={"key": issue.key, "comment_id": comment.id},
    )
    
    # Auto-watch for commenter
    watcher_add(issue=issue, user=author)
    
    return comment


@transaction.atomic
def comment_update(*, comment: Comment, content: str) -> Comment:
    """Update a comment."""
    comment.content = content
    comment.save()
    return comment


@transaction.atomic
def comment_delete(*, comment: Comment) -> None:
    """Delete a comment."""
    comment.delete()


@transaction.atomic
def attachment_create(
    *,
    issue: Issue,
    uploaded_by: User,
    file,
    filename: str,
    file_size: int,
    content_type: str,
) -> Attachment:
    """Create an attachment."""
    attachment = Attachment.objects.create(
        issue=issue,
        uploaded_by=uploaded_by,
        file=file,
        filename=filename,
        file_size=file_size,
        content_type=content_type,
    )
    
    # Create event
    event_create(
        project=issue.project,
        issue=issue,
        event_type=Event.EventType.ATTACHMENT_ADDED,
        actor=uploaded_by,
        data={"key": issue.key, "filename": filename},
    )
    
    return attachment


@transaction.atomic
def attachment_delete(*, attachment: Attachment) -> None:
    """Delete an attachment."""
    attachment.file.delete()
    attachment.delete()


@transaction.atomic
def watcher_add(*, issue: Issue, user: User) -> Watcher:
    """Add a watcher to an issue."""
    watcher, created = Watcher.objects.get_or_create(issue=issue, user=user)
    return watcher


@transaction.atomic
def watcher_remove(*, issue: Issue, user: User) -> None:
    """Remove a watcher from an issue."""
    Watcher.objects.filter(issue=issue, user=user).delete()


def event_create(
    *,
    project: Project,
    event_type: str,
    actor: User,
    issue: Issue = None,
    data: dict = None,
) -> Event:
    """Create an event for activity tracking."""
    return Event.objects.create(
        project=project,
        issue=issue,
        event_type=event_type,
        actor=actor,
        data=data or {},
    )
