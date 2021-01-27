"""
urls.py

Created on 2021-01-27
Updated on 2021-01-27

Copyright © Ryan Kan

Description: The file which contains the URLconf for the `console` app.
"""

# IMPORTS
from django.urls import path

from console import views

# URL CONFIG
app_name = "console"

urlpatterns = [
    path("console/", views.console_view, name="console"),
    path("execute-command/", views.execute_command_view, name="execute_command")
]
