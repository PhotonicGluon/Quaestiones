"""
views.py

Created on 2021-01-24
Updated on 2021-01-25

Copyright © Ryan Kan

Description: The views for the `leaderboard` app.
"""

# IMPORTS
from django.shortcuts import render


# VIEWS
def leaderboard_summary_view(request):
    return render(request, "leaderboard/summary.html")
