"""
Project views.
"""
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.projects.models import Board, Epic, Project, ProjectMembership, Sprint
from apps.projects.serializers import (
    BoardSerializer,
    EpicSerializer,
    ProjectCreateSerializer,
    ProjectDetailSerializer,
    ProjectMembershipSerializer,
    ProjectSerializer,
    SprintSerializer,
    WorkflowSerializer,
)
from common.permissions import IsProjectMember, IsProjectAdmin


class ProjectListCreateView(generics.ListCreateAPIView):
    """List and create projects."""
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return ProjectCreateSerializer
        return ProjectSerializer

    def get_queryset(self):
        from apps.projects.selectors import project_list
        return project_list(user=self.request.user)


class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a project."""
    permission_classes = [IsAuthenticated, IsProjectMember]
    serializer_class = ProjectDetailSerializer

    def get_queryset(self):
        from apps.projects.selectors import project_list
        return project_list(user=self.request.user)


class ProjectMemberListView(generics.ListCreateAPIView):
    """List and add project members."""
    serializer_class = ProjectMembershipSerializer
    permission_classes = [IsAuthenticated, IsProjectMember]

    def get_queryset(self):
        project_id = self.kwargs["project_id"]
        return ProjectMembership.objects.filter(project_id=project_id).select_related("user")

    def perform_create(self, serializer):
        from apps.projects.services import project_add_member
        from apps.projects.selectors import project_get_by_id
        from django.contrib.auth import get_user_model
        
        User = get_user_model()
        project = project_get_by_id(project_id=self.kwargs["project_id"])
        user = User.objects.get(id=serializer.validated_data["user_id"])
        role = serializer.validated_data.get("role", ProjectMembership.Role.MEMBER)
        
        project_add_member(project=project, user=user, role=role)


class ProjectMemberDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or remove a project member."""
    serializer_class = ProjectMembershipSerializer
    permission_classes = [IsAuthenticated, IsProjectAdmin]

    def get_queryset(self):
        project_id = self.kwargs["project_id"]
        return ProjectMembership.objects.filter(project_id=project_id).select_related("user")

    def perform_destroy(self, instance):
        from apps.projects.services import project_remove_member
        project_remove_member(project=instance.project, user=instance.user)


class BoardListCreateView(generics.ListCreateAPIView):
    """List and create boards for a project."""
    serializer_class = BoardSerializer
    permission_classes = [IsAuthenticated, IsProjectMember]

    def get_queryset(self):
        from apps.projects.selectors import board_list, project_get_by_id
        project = project_get_by_id(project_id=self.kwargs["project_id"])
        return board_list(project=project)

    def get_serializer_context(self):
        from apps.projects.selectors import project_get_by_id
        context = super().get_serializer_context()
        context["project"] = project_get_by_id(project_id=self.kwargs["project_id"])
        return context


class SprintListCreateView(generics.ListCreateAPIView):
    """List and create sprints."""
    serializer_class = SprintSerializer
    permission_classes = [IsAuthenticated, IsProjectMember]

    def get_queryset(self):
        from apps.projects.selectors import sprint_list, board_get_by_id
        board = board_get_by_id(board_id=self.kwargs.get("board_id"))
        status_filter = self.request.query_params.get("status")
        return sprint_list(board=board, status=status_filter)

    def get_serializer_context(self):
        from apps.projects.selectors import board_get_by_id
        context = super().get_serializer_context()
        context["board"] = board_get_by_id(board_id=self.kwargs.get("board_id"))
        return context


class SprintDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a sprint."""
    serializer_class = SprintSerializer
    permission_classes = [IsAuthenticated, IsProjectMember]

    def get_queryset(self):
        from apps.projects.selectors import sprint_list, board_get_by_id
        board = board_get_by_id(board_id=self.kwargs.get("board_id"))
        return sprint_list(board=board)


@api_view(["POST"])
@permission_classes([IsAuthenticated, IsProjectMember])
def sprint_start_view(request, board_id, sprint_id):
    """Start a sprint."""
    from apps.projects.services import sprint_start
    from apps.projects.selectors import sprint_get_by_id
    
    sprint = sprint_get_by_id(sprint_id=sprint_id)
    sprint = sprint_start(sprint=sprint)
    serializer = SprintSerializer(sprint)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated, IsProjectMember])
def sprint_close_view(request, board_id, sprint_id):
    """Close a sprint."""
    from apps.projects.services import sprint_close
    from apps.projects.selectors import sprint_get_by_id
    
    sprint = sprint_get_by_id(sprint_id=sprint_id)
    sprint = sprint_close(sprint=sprint)
    serializer = SprintSerializer(sprint)
    return Response(serializer.data)


class EpicListCreateView(generics.ListCreateAPIView):
    """List and create epics."""
    serializer_class = EpicSerializer
    permission_classes = [IsAuthenticated, IsProjectMember]

    def get_queryset(self):
        from apps.projects.selectors import epic_list, project_get_by_id
        project = project_get_by_id(project_id=self.kwargs["project_id"])
        return epic_list(project=project)

    def get_serializer_context(self):
        from apps.projects.selectors import project_get_by_id
        context = super().get_serializer_context()
        context["project"] = project_get_by_id(project_id=self.kwargs["project_id"])
        return context


class EpicDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete an epic."""
    serializer_class = EpicSerializer
    permission_classes = [IsAuthenticated, IsProjectMember]

    def get_queryset(self):
        from apps.projects.selectors import epic_list, project_get_by_id
        project = project_get_by_id(project_id=self.kwargs["project_id"])
        return epic_list(project=project)


@api_view(["GET"])
@permission_classes([IsAuthenticated, IsProjectMember])
def project_workflow_view(request, project_id):
    """Get project workflow."""
    from apps.projects.selectors import workflow_get_by_project, project_get_by_id
    
    project = project_get_by_id(project_id=project_id)
    workflow = workflow_get_by_project(project=project)
    serializer = WorkflowSerializer(workflow)
    return Response(serializer.data)
