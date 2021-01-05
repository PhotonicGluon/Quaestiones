"""
Quaestiones's Development Settings.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

# IMPORTS
from django.conf.urls.static import static

from Quaestiones.settings.common import *

# SETUP
print("!" * 10, "USING DEVELOPMENT SETTINGS", "!" * 10)

# DEVELOPMENT SPECIFIC SETTINGS
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/
DEBUG = True

ALLOWED_HOSTS = []

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
