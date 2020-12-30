"""
Quaestiones's Development Settings.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

# IMPORTS
from Quaestiones.settings.common import *

from django.conf.urls.static import static

# PRELOADING
print("!" * 10, "USING DEVELOPMENT SETTINGS", "!" * 10)

# DEVELOPMENT SPECIFIC SETTINGS
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/
DEBUG = True

ALLOWED_HOSTS = []
