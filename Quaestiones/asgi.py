"""
Quaestiones"s ASGI (Asynchronous Server Gateway Interface) Config.

It exposes the ASGI callable as a module-level variable named `application`.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""

# IMPORTS
import os

from django.core.asgi import get_asgi_application

# ASGI CONFIGURATION
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Quaestiones.settings.development")
application = get_asgi_application()
