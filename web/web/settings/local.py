from __future__ import absolute_import

from .base import *

DEBUG = True

ADMINS = (
    # ("Your Name", "your_email@example.com"),
)

MANAGERS = ADMINS

INSTALLED_APPS = INSTALLED_APPS + (
    'django_extensions',
    'debug_toolbar',
)

ALLOWED_HOSTS = [
    '*'
]
