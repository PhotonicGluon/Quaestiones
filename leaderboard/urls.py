"""
urls.py

Created on 2021-01-24
Updated on 2021-01-25

Copyright © Ryan Kan

Description: The file which contains the URLconf for the `accounts` app.
"""

# IMPORTS
from django.urls import path

from leaderboard import views

# URL CONFIG
app_name = "leaderboard"

urlpatterns = [
    path("summary/", views.leaderboard_summary_view, name="summary")
]
