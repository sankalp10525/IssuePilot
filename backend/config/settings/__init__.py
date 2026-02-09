"""
Django settings package.
Import appropriate settings module based on DJANGO_ENV environment variable.
"""
import os

env = os.environ.get("DJANGO_ENV", "dev")

if env == "prod":
    from .prod import *  # noqa
elif env == "test":
    from .test import *  # noqa
else:
    from .dev import *  # noqa
