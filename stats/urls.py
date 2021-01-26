"""
urls.py

Created on 2021-01-24
Updated on 2021-01-26

Copyright © Ryan Kan

Description: The file which contains the URLconf for the `stats` app.
"""

# IMPORTS
from django.urls import path

from Quaestiones.settings import ENABLE_LEADERBOARD
from Quaestiones.views import error404
from stats import views

# URL CONFIG
app_name = "stats"

urlpatterns = [
    path("leaderboard/", views.leaderboard_view if ENABLE_LEADERBOARD else error404,
         {"exception": "404"} if not ENABLE_LEADERBOARD else {}, name="leaderboard")
]
