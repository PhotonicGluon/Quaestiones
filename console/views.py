"""
views.py

Created on 2021-01-27
Updated on 2021-01-27

Copyright © Ryan Kan

Description: The views for the `console` app.
"""

# IMPORTS
import logging

from django.shortcuts import render

# SETUP
logger = logging.getLogger("Quaestiones")


# VIEWS
def console_view(request):
    return render(request, "console/console.html")
