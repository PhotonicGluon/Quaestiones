"""
Quaestiones's Production Settings.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

# IMPORTS
from Quaestiones.settings.common import *

# PRELOADING
print("-" * 10, "USING PRODUCTION SETTINGS", "-" * 10)

# PRODUCTION SPECIFIC SETTINGS
# Quick-start production settings
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/
DEBUG = False

# SECURITY WARNING: Update this when you have the production host!
ALLOWED_HOSTS = ["0.0.0.0", "127.0.0.1"]

# Logging
LOGGING["handlers"]["file"]["level"] = "INFO"
