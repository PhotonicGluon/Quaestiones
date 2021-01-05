"""
views.py

Created on 2021-01-05
Updated on 2021-01-05

Copyright © Ryan Kan

Description: The views of the main application.
"""

# IMPORTS
from django.shortcuts import render
from django.views.generic.base import RedirectView


# VIEWS
def info_view(request):
    return render(request, "Quaestiones/info.html")


# OTHER VIEWS
faviconView = RedirectView.as_view(url="/static/resources/img/favicon.ico", permanent=True)  # Where the favicon is
