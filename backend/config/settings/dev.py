"""
Development settings.
"""
from .base import *  # noqa

DEBUG = True

ALLOWED_HOSTS = ["*"]

# CORS - allow all origins in dev
CORS_ALLOW_ALL_ORIGINS = True

# Django Debug Toolbar (optional)
# INSTALLED_APPS += ["debug_toolbar"]  # noqa
# MIDDLEWARE = ["debug_toolbar.middleware.DebugToolbarMiddleware"] + MIDDLEWARE  # noqa
# INTERNAL_IPS = ["127.0.0.1"]

# Logging - more verbose in dev
LOGGING["loggers"]["django"]["level"] = "DEBUG"  # noqa
LOGGING["root"]["level"] = "DEBUG"  # noqa
