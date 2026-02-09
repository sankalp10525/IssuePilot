"""
API v1 URLs.
"""
from django.urls import include, path

urlpatterns = [
    # Auth & Users
    path("", include("apps.users.urls")),
    # Projects
    path("", include("apps.projects.urls")),
    # Issues
    path("", include("apps.issues.urls")),
    # Notifications
    path("", include("apps.notifications.urls")),
]
