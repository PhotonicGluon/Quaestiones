"""
development.py

Created on 2020-12-27
Updated on 2020-01-25

Copyright © Ryan Kan

Description: Quaestiones's development settings.
"""

# IMPORTS
from django.conf.urls.static import static

from Quaestiones.settings.common import *
from Quaestiones.settings.quaestiones import *

# SETUP
print("!" * 10, "USING DEVELOPMENT SETTINGS", "!" * 10)

# DEVELOPMENT SPECIFIC SETTINGS
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/
DEBUG = True

ALLOWED_HOSTS = []

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
