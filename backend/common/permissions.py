"""
Custom permissions.
"""
from rest_framework import permissions

from apps.projects.models import ProjectMembership


class IsProjectMember(permissions.BasePermission):
    """Check if user is a member of the project."""

    def has_permission(self, request, view):
        project_id = view.kwargs.get("project_id")
        if not project_id:
            return True
        
        return ProjectMembership.objects.filter(
            project_id=project_id,
            user=request.user
        ).exists()

    def has_object_permission(self, request, view, obj):
        # Handle different object types
        if hasattr(obj, "project"):
            project = obj.project
        elif hasattr(obj, "board"):
            project = obj.board.project
        elif hasattr(obj, "issue"):
            project = obj.issue.project
        else:
            project = obj
        
        return ProjectMembership.objects.filter(
            project=project,
            user=request.user
        ).exists()


class IsProjectAdmin(permissions.BasePermission):
    """Check if user is an admin or owner of the project."""

    def has_permission(self, request, view):
        project_id = view.kwargs.get("project_id")
        if not project_id:
            return True
        
        return ProjectMembership.objects.filter(
            project_id=project_id,
            user=request.user,
            role__in=[ProjectMembership.Role.OWNER, ProjectMembership.Role.ADMIN]
        ).exists()

    def has_object_permission(self, request, view, obj):
        if hasattr(obj, "project"):
            project = obj.project
        else:
            project = obj
        
        return ProjectMembership.objects.filter(
            project=project,
            user=request.user,
            role__in=[ProjectMembership.Role.OWNER, ProjectMembership.Role.ADMIN]
        ).exists()


class IsProjectOwner(permissions.BasePermission):
    """Check if user is the owner of the project."""

    def has_object_permission(self, request, view, obj):
        if hasattr(obj, "project"):
            project = obj.project
        else:
            project = obj
        
        return project.owner == request.user
