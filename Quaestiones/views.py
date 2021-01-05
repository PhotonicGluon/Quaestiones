"""
views.py

Created on 2021-01-05
Updated on 2021-01-05

Copyright © Ryan Kan

Description: The views of the main application.
"""

# IMPORTS
from django.views.generic.base import RedirectView

# VIEWS
faviconView = RedirectView.as_view(url="/static/resources/img/favicon.ico", permanent=True)  # Where the favicon is
