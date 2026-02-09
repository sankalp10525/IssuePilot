"""
Issue URLs.
"""
from django.urls import path

from apps.issues.views import (
    AttachmentDetailView,
    AttachmentListCreateView,
    CommentDetailView,
    CommentListCreateView,
    IssueDetailView,
    IssueListCreateView,
    issue_activity_view,
    issue_transition_view,
    project_activity_view,
    watchers_view,
)

urlpatterns = [
    # Issues
    path("projects/<int:project_id>/issues/", IssueListCreateView.as_view(), name="issue-list"),
    path("projects/<int:project_id>/issues/<str:issue_key>/", IssueDetailView.as_view(), name="issue-detail"),
    path("projects/<int:project_id>/issues/<str:issue_key>/transitions/", issue_transition_view, name="issue-transition"),
    # Comments
    path("projects/<int:project_id>/issues/<str:issue_key>/comments/", CommentListCreateView.as_view(), name="comment-list"),
    path("projects/<int:project_id>/issues/<str:issue_key>/comments/<int:pk>/", CommentDetailView.as_view(), name="comment-detail"),
    # Attachments
    path("projects/<int:project_id>/issues/<str:issue_key>/attachments/", AttachmentListCreateView.as_view(), name="attachment-list"),
    path("projects/<int:project_id>/issues/<str:issue_key>/attachments/<int:pk>/", AttachmentDetailView.as_view(), name="attachment-detail"),
    # Watchers
    path("projects/<int:project_id>/issues/<str:issue_key>/watchers/", watchers_view, name="watchers"),
    # Activity
    path("projects/<int:project_id>/activity/", project_activity_view, name="project-activity"),
    path("projects/<int:project_id>/issues/<str:issue_key>/activity/", issue_activity_view, name="issue-activity"),
]
