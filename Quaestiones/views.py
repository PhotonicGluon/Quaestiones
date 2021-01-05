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


# ERROR VIEWS
def error400(request, exception):
    # 'Delete' unused variables
    _ = exception

    return render(request, "global/400.html")


def error403(request, exception):
    # 'Delete' unused variables
    _ = exception

    return render(request, "global/403.html")


def error404(request, exception):
    # 'Delete' unused variables
    _ = exception

    return render(request, "global/404.html")


def error500(request):
    return render(request, "global/500.html")


# OTHER VIEWS
faviconView = RedirectView.as_view(url="/static/resources/img/favicon.ico", permanent=True)  # Where the favicon is
