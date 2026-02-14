"""
Test settings.
"""
from .base import *  # noqa

DEBUG = False

# Use faster password hasher for tests
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]

# In-memory database for faster tests
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

# Disable migrations for faster tests
class DisableMigrations:
    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        return None


MIGRATION_MODULES = DisableMigrations()

# Celery - use eager mode for tests
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True

# Email - use memory backend
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

# Logging - reduce noise in tests
LOGGING["root"]["level"] = "ERROR"  # noqa
LOGGING["loggers"]["django"]["level"] = "ERROR"  # noqa
