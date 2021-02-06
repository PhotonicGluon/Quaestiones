"""
common.py

Created on 2020-12-27
Updated on 2020-02-06

Copyright © Ryan Kan

Description: Quaestiones's Common Settings.

References:
    - https://docs.djangoproject.com/en/3.0/topics/settings/
    - https://docs.djangoproject.com/en/3.0/ref/settings/
"""

# IMPORTS
import os

# SETUP
# Get needed directories
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SECRET_FILES_DIR = os.path.join(BASE_DIR, "Quaestiones/SecretFiles")

# SETTINGS
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = open(os.path.join(SECRET_FILES_DIR, "secret.txt"), "r").read().strip()
TIMEOUT = 60

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.humanize",
    "django.contrib.messages",
    "django.contrib.sessions",
    "whitenoise.runserver_nostatic",
    "django.contrib.staticfiles",
    "accounts.apps.AccountsConfig",
    "console.apps.ConsoleConfig",
    "misc.apps.MiscConfig",
    "stats.apps.StatsConfig",
    "questions.apps.QuestionsConfig",
    "upload_file.apps.UploadFileConfig"
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "Quaestiones.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "Quaestiones/templates")
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages"
            ],
        },
    },
]

ASGI_APPLICATION = "Quaestiones.asgi.application"

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "Quaestiones/Database.sqlite"),
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/
LANGUAGE_CODE = "en-gb"
TIME_ZONE = "Asia/Singapore"

USE_I18N = True  # i18n --> Internationalisation
USE_L10N = True  # l10n --> localisation
USE_TZ = True  # tz --> timezones

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/
STATIC_URL = "/static/"
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "Assets"),  # This is where all our assets will be stored
)
STATIC_ROOT = os.path.join(BASE_DIR, "Staticfiles")  # Run `python manage.py collectstatic` before deploying
STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"

# Media files
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "MediaFiles")
QUESTION_INPUT_ROOT = os.path.join(MEDIA_ROOT, "Question-Inputs")
UPLOADED_FILES_ROOT = os.path.join(MEDIA_ROOT, "Uploaded-Files")

# Logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "[{asctime}] ({module}) {levelname}: {message}",
            "datefmt": "%Y-%m-%d %H:%M:%S UTC%Z",
            "style": "{",
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default"
        },
        "file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "formatter": "default",
            "filename": "Logs/Quaestiones.log",
        }
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
        "propagate": True,
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": True,
        },

        "Quaestiones": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": True
        }
    }
}

# Messages
MESSAGE_STORAGE = "django.contrib.messages.storage.cookie.CookieStorage"
