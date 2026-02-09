"""
Project URLs.
"""
from django.urls import path

from apps.projects.views import (
    BoardListCreateView,
    EpicDetailView,
    EpicListCreateView,
    ProjectDetailView,
    ProjectListCreateView,
    ProjectMemberDetailView,
    ProjectMemberListView,
    SprintDetailView,
    SprintListCreateView,
    project_workflow_view,
    sprint_close_view,
    sprint_start_view,
)

urlpatterns = [
    # Projects
    path("projects/", ProjectListCreateView.as_view(), name="project-list"),
    path("projects/<int:pk>/", ProjectDetailView.as_view(), name="project-detail"),
    path("projects/<int:project_id>/members/", ProjectMemberListView.as_view(), name="project-member-list"),
    path("projects/<int:project_id>/members/<int:pk>/", ProjectMemberDetailView.as_view(), name="project-member-detail"),
    path("projects/<int:project_id>/boards/", BoardListCreateView.as_view(), name="board-list"),
    path("projects/<int:project_id>/epics/", EpicListCreateView.as_view(), name="epic-list"),
    path("projects/<int:project_id>/epics/<int:pk>/", EpicDetailView.as_view(), name="epic-detail"),
    path("projects/<int:project_id>/workflow/", project_workflow_view, name="project-workflow"),
    # Sprints
    path("boards/<int:board_id>/sprints/", SprintListCreateView.as_view(), name="sprint-list"),
    path("boards/<int:board_id>/sprints/<int:pk>/", SprintDetailView.as_view(), name="sprint-detail"),
    path("boards/<int:board_id>/sprints/<int:sprint_id>/start/", sprint_start_view, name="sprint-start"),
    path("boards/<int:board_id>/sprints/<int:sprint_id>/close/", sprint_close_view, name="sprint-close"),
]
