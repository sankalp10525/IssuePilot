"""
Project services.
"""
from django.contrib.auth import get_user_model
from django.db import transaction

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


@transaction.atomic
def project_create(
    *,
    name: str,
    key: str,
    owner: User,
    description: str = "",
    icon: str = "",
) -> Project:
    """Create a new project with default workflow."""
    project = Project.objects.create(
        name=name,
        key=key.upper(),
        description=description,
        icon=icon,
        owner=owner,
    )
    
    # Create owner membership
    ProjectMembership.objects.create(
        project=project,
        user=owner,
        role=ProjectMembership.Role.OWNER,
    )
    
    # Create default workflow
    workflow = Workflow.objects.create(
        project=project,
        name="Default Workflow",
    )
    
    # Create default states
    todo = WorkflowState.objects.create(
        workflow=workflow,
        name="To Do",
        category=WorkflowState.Category.TODO,
        order=0,
        is_initial=True,
    )
    in_progress = WorkflowState.objects.create(
        workflow=workflow,
        name="In Progress",
        category=WorkflowState.Category.IN_PROGRESS,
        order=1,
    )
    done = WorkflowState.objects.create(
        workflow=workflow,
        name="Done",
        category=WorkflowState.Category.DONE,
        order=2,
    )
    
    # Create default transitions
    WorkflowTransition.objects.create(
        workflow=workflow,
        from_state=todo,
        to_state=in_progress,
        name="Start Progress",
    )
    WorkflowTransition.objects.create(
        workflow=workflow,
        from_state=in_progress,
        to_state=done,
        name="Complete",
    )
    WorkflowTransition.objects.create(
        workflow=workflow,
        from_state=in_progress,
        to_state=todo,
        name="Move to Backlog",
    )
    WorkflowTransition.objects.create(
        workflow=workflow,
        from_state=done,
        to_state=in_progress,
        name="Reopen",
    )
    
    # Create default board
    Board.objects.create(
        project=project,
        name=f"{project.name} Board",
        board_type=Board.BoardType.KANBAN,
    )
    
    return project


@transaction.atomic
def project_update(*, project: Project, **data) -> Project:
    """Update project."""
    for field, value in data.items():
        setattr(project, field, value)
    project.save()
    return project


@transaction.atomic
def project_delete(*, project: Project) -> None:
    """Delete a project."""
    project.delete()


@transaction.atomic
def project_add_member(
    *,
    project: Project,
    user: User,
    role: str = ProjectMembership.Role.MEMBER,
) -> ProjectMembership:
    """Add a member to project."""
    membership, created = ProjectMembership.objects.get_or_create(
        project=project,
        user=user,
        defaults={"role": role},
    )
    if not created:
        membership.role = role
        membership.save()
    return membership


@transaction.atomic
def project_remove_member(*, project: Project, user: User) -> None:
    """Remove a member from project."""
    ProjectMembership.objects.filter(project=project, user=user).delete()


@transaction.atomic
def board_create(*, project: Project, name: str, board_type: str) -> Board:
    """Create a new board."""
    return Board.objects.create(
        project=project,
        name=name,
        board_type=board_type,
    )


@transaction.atomic
def board_update(*, board: Board, **data) -> Board:
    """Update board."""
    for field, value in data.items():
        setattr(board, field, value)
    board.save()
    return board


@transaction.atomic
def sprint_create(
    *,
    board: Board,
    name: str,
    goal: str = "",
    start_date=None,
    end_date=None,
) -> Sprint:
    """Create a new sprint."""
    return Sprint.objects.create(
        board=board,
        name=name,
        goal=goal,
        start_date=start_date,
        end_date=end_date,
    )


@transaction.atomic
def sprint_update(*, sprint: Sprint, **data) -> Sprint:
    """Update sprint."""
    for field, value in data.items():
        setattr(sprint, field, value)
    sprint.save()
    return sprint


@transaction.atomic
def sprint_start(*, sprint: Sprint) -> Sprint:
    """Start a sprint."""
    sprint.status = Sprint.Status.ACTIVE
    sprint.save()
    return sprint


@transaction.atomic
def sprint_close(*, sprint: Sprint) -> Sprint:
    """Close a sprint."""
    sprint.status = Sprint.Status.CLOSED
    sprint.save()
    return sprint


@transaction.atomic
def epic_create(
    *,
    project: Project,
    name: str,
    description: str = "",
    color: str = "#6B7280",
    start_date=None,
    due_date=None,
) -> Epic:
    """Create a new epic."""
    return Epic.objects.create(
        project=project,
        name=name,
        description=description,
        color=color,
        start_date=start_date,
        due_date=due_date,
    )


@transaction.atomic
def epic_update(*, epic: Epic, **data) -> Epic:
    """Update epic."""
    for field, value in data.items():
        setattr(epic, field, value)
    epic.save()
    return epic


@transaction.atomic
def workflow_state_create(
    *,
    workflow: Workflow,
    name: str,
    category: str,
    order: int = 0,
    is_initial: bool = False,
) -> WorkflowState:
    """Create a new workflow state."""
    if is_initial:
        # Ensure only one initial state
        WorkflowState.objects.filter(workflow=workflow, is_initial=True).update(is_initial=False)
    
    return WorkflowState.objects.create(
        workflow=workflow,
        name=name,
        category=category,
        order=order,
        is_initial=is_initial,
    )


@transaction.atomic
def workflow_transition_create(
    *,
    workflow: Workflow,
    from_state: WorkflowState,
    to_state: WorkflowState,
    name: str = "",
) -> WorkflowTransition:
    """Create a new workflow transition."""
    return WorkflowTransition.objects.create(
        workflow=workflow,
        from_state=from_state,
        to_state=to_state,
        name=name,
    )
