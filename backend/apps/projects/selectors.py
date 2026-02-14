"""
Project selectors.
"""
from django.contrib.auth import get_user_model
from django.db.models import Prefetch, Q, QuerySet

from apps.projects.models import (
    Board,
    Epic,
    Project,
    ProjectMembership,
    Sprint,
    Workflow,
    WorkflowState,
    WorkflowTransition,
)

User = get_user_model()


def project_list(*, user: User) -> QuerySet:
    """Get all projects accessible to user."""
    return Project.objects.filter(
        memberships__user=user
    ).select_related("owner").prefetch_related("memberships__user")


def project_get_by_id(*, project_id: int) -> Project:
    """Get project by ID."""
    return Project.objects.select_related("owner", "workflow").get(id=project_id)


def project_get_by_key(*, key: str) -> Project:
    """Get project by key."""
    return Project.objects.select_related("owner", "workflow").get(key=key)


def project_has_member(*, project: Project, user: User) -> bool:
    """Check if user is a member of project."""
    return ProjectMembership.objects.filter(project=project, user=user).exists()


def project_get_membership(*, project: Project, user: User) -> ProjectMembership:
    """Get user's membership in project."""
    return ProjectMembership.objects.get(project=project, user=user)


def board_list(*, project: Project) -> QuerySet:
    """Get all boards for a project."""
    return Board.objects.filter(project=project)


def board_get_by_id(*, board_id: int) -> Board:
    """Get board by ID."""
    return Board.objects.select_related("project").get(id=board_id)


def sprint_list(*, board: Board, status: str = None) -> QuerySet:
    """Get sprints for a board."""
    qs = Sprint.objects.filter(board=board)
    if status:
        qs = qs.filter(status=status)
    return qs


def sprint_get_by_id(*, sprint_id: int) -> Sprint:
    """Get sprint by ID."""
    return Sprint.objects.select_related("board__project").get(id=sprint_id)


def epic_list(*, project: Project) -> QuerySet:
    """Get all epics for a project."""
    return Epic.objects.filter(project=project)


def epic_get_by_id(*, epic_id: int) -> Epic:
    """Get epic by ID."""
    return Epic.objects.select_related("project").get(id=epic_id)


def workflow_get_by_project(*, project: Project) -> Workflow:
    """Get workflow for a project."""
    return Workflow.objects.prefetch_related(
        "states",
        "transitions__from_state",
        "transitions__to_state"
    ).get(project=project)


def workflow_state_list(*, workflow: Workflow) -> QuerySet:
    """Get all states in a workflow."""
    return WorkflowState.objects.filter(workflow=workflow)


def workflow_get_initial_state(*, workflow: Workflow) -> WorkflowState:
    """Get initial state of a workflow."""
    return WorkflowState.objects.get(workflow=workflow, is_initial=True)


def workflow_get_allowed_transitions(*, from_state: WorkflowState) -> QuerySet:
    """Get allowed transitions from a state."""
    return WorkflowTransition.objects.filter(
        from_state=from_state
    ).select_related("to_state")


def workflow_can_transition(*, from_state: WorkflowState, to_state: WorkflowState) -> bool:
    """Check if transition is allowed."""
    return WorkflowTransition.objects.filter(
        from_state=from_state,
        to_state=to_state
    ).exists()
