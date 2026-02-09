"""
Project admin configuration.
"""
from django.contrib import admin

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


class ProjectMembershipInline(admin.TabularInline):
    model = ProjectMembership
    extra = 0
    autocomplete_fields = ["user"]


class BoardInline(admin.TabularInline):
    model = Board
    extra = 0


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ["key", "name", "owner", "created_at"]
    list_filter = ["created_at"]
    search_fields = ["name", "key", "description"]
    autocomplete_fields = ["owner"]
    inlines = [ProjectMembershipInline, BoardInline]
    readonly_fields = ["created_at", "updated_at"]


@admin.register(ProjectMembership)
class ProjectMembershipAdmin(admin.ModelAdmin):
    list_display = ["project", "user", "role", "created_at"]
    list_filter = ["role", "created_at"]
    search_fields = ["project__name", "user__username"]
    autocomplete_fields = ["project", "user"]


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ["name", "project", "board_type", "created_at"]
    list_filter = ["board_type", "created_at"]
    search_fields = ["name", "project__name"]
    autocomplete_fields = ["project"]


@admin.register(Sprint)
class SprintAdmin(admin.ModelAdmin):
    list_display = ["name", "board", "status", "start_date", "end_date"]
    list_filter = ["status", "start_date"]
    search_fields = ["name", "board__name"]
    autocomplete_fields = ["board"]
    readonly_fields = ["created_at", "updated_at"]


@admin.register(Epic)
class EpicAdmin(admin.ModelAdmin):
    list_display = ["name", "project", "start_date", "due_date", "created_at"]
    list_filter = ["created_at"]
    search_fields = ["name", "project__name"]
    autocomplete_fields = ["project"]
    readonly_fields = ["created_at", "updated_at"]


class WorkflowStateInline(admin.TabularInline):
    model = WorkflowState
    extra = 0
    ordering = ["order"]


class WorkflowTransitionInline(admin.TabularInline):
    model = WorkflowTransition
    extra = 0
    fk_name = "workflow"
    autocomplete_fields = ["from_state", "to_state"]


@admin.register(Workflow)
class WorkflowAdmin(admin.ModelAdmin):
    list_display = ["name", "project", "created_at"]
    search_fields = ["name", "project__name"]
    autocomplete_fields = ["project"]
    inlines = [WorkflowStateInline, WorkflowTransitionInline]
    readonly_fields = ["created_at", "updated_at"]


@admin.register(WorkflowState)
class WorkflowStateAdmin(admin.ModelAdmin):
    list_display = ["name", "workflow", "category", "order", "is_initial"]
    list_filter = ["category", "is_initial"]
    search_fields = ["name", "workflow__name"]
    autocomplete_fields = ["workflow"]
    ordering = ["workflow", "order"]


@admin.register(WorkflowTransition)
class WorkflowTransitionAdmin(admin.ModelAdmin):
    list_display = ["workflow", "from_state", "to_state", "name"]
    search_fields = ["name", "workflow__name"]
    autocomplete_fields = ["workflow", "from_state", "to_state"]
