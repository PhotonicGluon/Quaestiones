"""
development.py

Created on 2020-12-27
Updated on 2020-01-25

Copyright © Ryan Kan

Description: Quaestiones's production settings.
"""

# IMPORTS
import yaml

from Quaestiones.settings.common import *
from Quaestiones.settings.quaestiones import *

# SETUP
print("-" * 10, "USING PRODUCTION SETTINGS", "-" * 10)

# Load email credentials
emailConfig = yaml.load(open(os.path.join(SECRET_FILES_DIR, "email_credentials.yaml"), "r"), Loader=yaml.Loader)

# PRODUCTION SPECIFIC SETTINGS
# Quick-start production settings
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/
DEBUG = False

# SECURITY WARNING: Update this when you have the production host!
ALLOWED_HOSTS = ["0.0.0.0", "127.0.0.1"]

# Logging
LOGGING["handlers"]["file"]["level"] = "INFO"

# Email
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = emailConfig["email_host"]
EMAIL_USE_TLS = emailConfig["email_use_tls"]
EMAIL_PORT = emailConfig["email_port"]
EMAIL_HOST_USER = emailConfig["email_user"]
EMAIL_HOST_PASSWORD = emailConfig["email_password"]
