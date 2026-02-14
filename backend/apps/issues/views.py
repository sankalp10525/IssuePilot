"""
Issue views.
"""
from django_filters import rest_framework as filters
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.issues.models import Attachment, Comment, Issue
from apps.issues.serializers import (
    AttachmentSerializer,
    CommentSerializer,
    EventSerializer,
    IssueCreateSerializer,
    IssueDetailSerializer,
    IssueListSerializer,
    IssueTransitionSerializer,
    IssueUpdateSerializer,
)
from common.permissions import IsProjectMember


class IssueFilter(filters.FilterSet):
    """Filter for issues."""
    state = filters.NumberFilter(field_name="state__id")
    assignee = filters.NumberFilter(field_name="assignee__id")
    reporter = filters.NumberFilter(field_name="reporter__id")
    sprint = filters.NumberFilter(field_name="sprint__id")
    epic = filters.NumberFilter(field_name="epic__id")
    issue_type = filters.ChoiceFilter(choices=Issue.Type.choices)
    priority = filters.ChoiceFilter(choices=Issue.Priority.choices)

    class Meta:
        model = Issue
        fields = ["state", "assignee", "reporter", "sprint", "epic", "issue_type", "priority"]


class IssueListCreateView(generics.ListCreateAPIView):
    """List and create issues."""
    permission_classes = [IsAuthenticated, IsProjectMember]
    filterset_class = IssueFilter
    search_fields = ["key", "title", "description"]
    ordering_fields = ["created_at", "updated_at", "priority"]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return IssueCreateSerializer
        return IssueListSerializer

    def get_queryset(self):
        from apps.issues.selectors import issue_list, issue_search
        from apps.projects.selectors import project_get_by_id
        
        project = project_get_by_id(project_id=self.kwargs["project_id"])
        
        # Handle search
        search_query = self.request.query_params.get("q")
        if search_query:
            return issue_search(project=project, query=search_query)
        
        return issue_list(project=project)

    def get_serializer_context(self):
        from apps.projects.selectors import project_get_by_id
        context = super().get_serializer_context()
        context["project"] = project_get_by_id(project_id=self.kwargs["project_id"])
        return context


class IssueDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete an issue."""
    permission_classes = [IsAuthenticated, IsProjectMember]
    lookup_field = "key"
    lookup_url_kwarg = "issue_key"

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return IssueUpdateSerializer
        return IssueDetailSerializer

    def get_queryset(self):
        from apps.issues.selectors import issue_list
        from apps.projects.selectors import project_get_by_id
        
        project = project_get_by_id(project_id=self.kwargs["project_id"])
        return issue_list(project=project)

    def perform_destroy(self, instance):
        from apps.issues.services import issue_delete
        issue_delete(issue=instance, actor=self.request.user)


class CommentListCreateView(generics.ListCreateAPIView):
    """List and create comments on an issue."""
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsProjectMember]

    def get_queryset(self):
        from apps.issues.selectors import comment_list, issue_get_by_key
        issue = issue_get_by_key(key=self.kwargs["issue_key"])
        return comment_list(issue=issue)

    def get_serializer_context(self):
        from apps.issues.selectors import issue_get_by_key
        context = super().get_serializer_context()
        context["issue"] = issue_get_by_key(key=self.kwargs["issue_key"])
        return context


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a comment."""
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsProjectMember]

    def get_queryset(self):
        return Comment.objects.all()

    def get_serializer_context(self):
        from apps.issues.selectors import issue_get_by_key
        context = super().get_serializer_context()
        context["issue"] = issue_get_by_key(key=self.kwargs["issue_key"])
        return context


class AttachmentListCreateView(generics.ListCreateAPIView):
    """List and upload attachments for an issue."""
    serializer_class = AttachmentSerializer
    permission_classes = [IsAuthenticated, IsProjectMember]
    parser_classes = [MultiPartParser]

    def get_queryset(self):
        from apps.issues.selectors import attachment_list, issue_get_by_key
        issue = issue_get_by_key(key=self.kwargs["issue_key"])
        return attachment_list(issue=issue)

    def get_serializer_context(self):
        from apps.issues.selectors import issue_get_by_key
        context = super().get_serializer_context()
        context["issue"] = issue_get_by_key(key=self.kwargs["issue_key"])
        return context


class AttachmentDetailView(generics.RetrieveDestroyAPIView):
    """Retrieve or delete an attachment."""
    serializer_class = AttachmentSerializer
    permission_classes = [IsAuthenticated, IsProjectMember]

    def get_queryset(self):
        return Attachment.objects.all()

    def perform_destroy(self, instance):
        from apps.issues.services import attachment_delete
        attachment_delete(attachment=instance)


@api_view(["GET", "POST", "DELETE"])
@permission_classes([IsAuthenticated, IsProjectMember])
def watchers_view(request, project_id, issue_key):
    """List, add, or remove watchers."""
    from apps.issues.selectors import issue_get_by_key, watcher_list
    from apps.issues.services import watcher_add, watcher_remove
    
    issue = issue_get_by_key(key=issue_key)
    
    if request.method == "GET":
        from apps.issues.serializers import WatcherSerializer
        watchers = watcher_list(issue=issue)
        serializer = WatcherSerializer(watchers, many=True)
        return Response(serializer.data)
    
    elif request.method == "POST":
        watcher = watcher_add(issue=issue, user=request.user)
        from apps.issues.serializers import WatcherSerializer
        serializer = WatcherSerializer(watcher)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    elif request.method == "DELETE":
        watcher_remove(issue=issue, user=request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["POST"])
@permission_classes([IsAuthenticated, IsProjectMember])
def issue_transition_view(request, project_id, issue_key):
    """Transition issue to a new state."""
    from apps.issues.selectors import issue_get_by_key
    from apps.issues.services import issue_transition
    from apps.projects.models import WorkflowState
    
    issue = issue_get_by_key(key=issue_key)
    serializer = IssueTransitionSerializer(data=request.data, context={"issue": issue})
    serializer.is_valid(raise_exception=True)
    
    to_state = WorkflowState.objects.get(id=serializer.validated_data["to_state_id"])
    issue = issue_transition(issue=issue, to_state=to_state, actor=request.user)
    
    response_serializer = IssueDetailSerializer(issue, context={"request": request})
    return Response(response_serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated, IsProjectMember])
def project_activity_view(request, project_id):
    """Get activity feed for a project."""
    from apps.issues.selectors import event_list_by_project
    from apps.projects.selectors import project_get_by_id
    
    project = project_get_by_id(project_id=project_id)
    events = event_list_by_project(project=project, limit=100)
    serializer = EventSerializer(events, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated, IsProjectMember])
def issue_activity_view(request, project_id, issue_key):
    """Get activity feed for an issue."""
    from apps.issues.selectors import event_list_by_issue, issue_get_by_key
    
    issue = issue_get_by_key(key=issue_key)
    events = event_list_by_issue(issue=issue)
    serializer = EventSerializer(events, many=True)
    return Response(serializer.data)
