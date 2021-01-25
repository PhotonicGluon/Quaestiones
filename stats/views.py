"""
views.py

Created on 2021-01-24
Updated on 2021-01-25

Copyright © Ryan Kan

Description: The views for the `stats` app.
"""

# IMPORTS
import logging

from django.http import HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import render
from ratelimit import ALL as RATELIMIT_ALL
from ratelimit.decorators import ratelimit

from Quaestiones.settings import NUM_USERS_TO_SHOW

# SETUP
logger = logging.getLogger("Quaestiones")


# VIEWS
# Main Views
@ratelimit(key="ip", rate="3/s", method=RATELIMIT_ALL)
def leaderboard_view(request):
    # Get the top `NUM_USERS_TO_SHOW` users
    top_users = User.objects.order_by("-profile__total_score")[:NUM_USERS_TO_SHOW]

    # Pass that information to the template
    return render(request, "stats/leaderboard.html", {"num_users_to_show": NUM_USERS_TO_SHOW, "top_users": top_users})


# Other Views
def plea_for_no_automated_requests(request):
    logger.warning(f"Someone from the IP address {request.META['REMOTE_ADDR']} is sending too many requests!")
    return HttpResponse("Please do not send requests this fast to the website! You'll make me sad if you do :(",
                        content_type="text/plain")
