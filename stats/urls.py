"""
urls.py

Created on 2021-01-24
Updated on 2021-01-25

Copyright © Ryan Kan

Description: The file which contains the URLconf for the `stats` app.
"""

# IMPORTS
from django.urls import path

from stats import views

# URL CONFIG
app_name = "stats"

urlpatterns = [
    path("leaderboard/", views.leaderboard_view, name="leaderboard")
]
