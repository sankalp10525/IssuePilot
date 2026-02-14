"""
Issue admin configuration.
"""
from django.contrib import admin

from apps.issues.models import Attachment, Comment, Event, Issue, Watcher


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ["key", "title", "issue_type", "priority", "state", "assignee", "created_at"]
    list_filter = ["issue_type", "priority", "state", "created_at"]
    search_fields = ["key", "title", "description"]
    autocomplete_fields = ["project", "reporter", "assignee", "sprint", "epic", "parent", "state"]
    readonly_fields = ["key", "sequence", "created_at", "updated_at", "resolved_at"]
    
    fieldsets = (
        ("Identification", {
            "fields": ("project", "key", "sequence")
        }),
        ("Content", {
            "fields": ("title", "description", "issue_type", "priority")
        }),
        ("Workflow", {
            "fields": ("state",)
        }),
        ("Relationships", {
            "fields": ("sprint", "epic", "parent")
        }),
        ("People", {
            "fields": ("reporter", "assignee")
        }),
        ("Estimates", {
            "fields": ("story_points", "time_estimate", "time_spent")
        }),
        ("Dates", {
            "fields": ("due_date", "resolved_at", "created_at", "updated_at")
        }),
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["issue", "author", "created_at"]
    list_filter = ["created_at"]
    search_fields = ["content", "issue__key"]
    autocomplete_fields = ["issue", "author"]
    readonly_fields = ["created_at", "updated_at"]


@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    list_display = ["filename", "issue", "uploaded_by", "file_size", "created_at"]
    list_filter = ["content_type", "created_at"]
    search_fields = ["filename", "issue__key"]
    autocomplete_fields = ["issue", "uploaded_by"]
    readonly_fields = ["created_at"]


@admin.register(Watcher)
class WatcherAdmin(admin.ModelAdmin):
    list_display = ["issue", "user", "created_at"]
    list_filter = ["created_at"]
    search_fields = ["issue__key", "user__username"]
    autocomplete_fields = ["issue", "user"]
    readonly_fields = ["created_at"]


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ["event_type", "project", "issue", "actor", "created_at"]
    list_filter = ["event_type", "created_at"]
    search_fields = ["issue__key", "actor__username"]
    autocomplete_fields = ["project", "issue", "actor"]
    readonly_fields = ["created_at"]
