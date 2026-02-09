"""
Notification serializers.
"""
from rest_framework import serializers

from apps.notifications.models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    """Notification serializer."""
    project_key = serializers.CharField(source="project.key", read_only=True, allow_null=True)
    issue_key = serializers.CharField(source="issue.key", read_only=True, allow_null=True)

    class Meta:
        model = Notification
        fields = [
            "id",
            "notification_type",
            "title",
            "message",
            "project_key",
            "issue_key",
            "is_read",
            "read_at",
            "created_at",
        ]
        read_only_fields = ["id", "created_at", "read_at"]
