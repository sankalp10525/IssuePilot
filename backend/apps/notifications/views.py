"""
Notification views.
"""
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.notifications.models import Notification
from apps.notifications.serializers import NotificationSerializer


class NotificationListView(generics.ListAPIView):
    """List notifications for current user."""
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        from apps.notifications.selectors import notification_list
        
        is_read = self.request.query_params.get("is_read")
        if is_read is not None:
            is_read = is_read.lower() == "true"
        
        return notification_list(user=self.request.user, is_read=is_read)


class NotificationDetailView(generics.RetrieveUpdateAPIView):
    """Retrieve or update a notification."""
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user)

    def perform_update(self, serializer):
        from apps.notifications.services import notification_mark_read
        notification = serializer.instance
        notification_mark_read(notification=notification)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def notification_unread_count_view(request):
    """Get unread notification count."""
    from apps.notifications.selectors import notification_unread_count
    count = notification_unread_count(user=request.user)
    return Response({"count": count})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def notification_mark_all_read_view(request):
    """Mark all notifications as read."""
    from apps.notifications.services import notification_mark_all_read
    count = notification_mark_all_read(user=request.user)
    return Response({"marked_read": count})
