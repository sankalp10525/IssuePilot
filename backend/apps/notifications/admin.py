"""
Notification admin configuration.
"""
from django.contrib import admin

from apps.notifications.models import Notification, OutboxMessage


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ["title", "recipient", "notification_type", "is_read", "created_at"]
    list_filter = ["notification_type", "is_read", "created_at"]
    search_fields = ["title", "message", "recipient__username"]
    autocomplete_fields = ["recipient", "project", "issue"]
    readonly_fields = ["created_at", "read_at"]


@admin.register(OutboxMessage)
class OutboxMessageAdmin(admin.ModelAdmin):
    list_display = ["event_type", "status", "retry_count", "created_at", "processed_at"]
    list_filter = ["status", "event_type", "created_at"]
    search_fields = ["event_type", "error_message"]
    readonly_fields = ["created_at", "processed_at"]
