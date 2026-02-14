"""
Notification URLs.
"""
from django.urls import path

from apps.notifications.views import (
    NotificationDetailView,
    NotificationListView,
    notification_mark_all_read_view,
    notification_unread_count_view,
)

urlpatterns = [
    path("notifications/", NotificationListView.as_view(), name="notification-list"),
    path("notifications/unread-count/", notification_unread_count_view, name="notification-unread-count"),
    path("notifications/mark-all-read/", notification_mark_all_read_view, name="notification-mark-all-read"),
    path("notifications/<int:pk>/", NotificationDetailView.as_view(), name="notification-detail"),
]
