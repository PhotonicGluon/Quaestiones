"""
views.py

Created on 2021-01-24
Updated on 2021-01-25

Copyright © Ryan Kan

Description: The views for the `stats` app.
"""

# IMPORTS
import logging

from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render
from ratelimit import ALL as RATELIMIT_ALL
from ratelimit.decorators import ratelimit

from Quaestiones.settings import NUM_USERS_TO_SHOW
from accounts.models import Profile

# SETUP
logger = logging.getLogger("Quaestiones")


# VIEWS
# Main Views
@ratelimit(key="ip", rate="3/s", method=RATELIMIT_ALL)
def leaderboard_view(request):
    # Order all the users by the total score
    users_sorted_by_score = User.objects.order_by("-profile__total_score")

    # Get the top `NUM_USERS_TO_SHOW` users
    top_users = users_sorted_by_score[:NUM_USERS_TO_SHOW]

    # Get everyone's position
    positions = list(range(1, len(top_users) + 1))
    previous_score = top_users[0].profile.total_score

    for i, user in enumerate(top_users[1:], start=1):
        current_score = user.profile.total_score

        if current_score == previous_score:
            positions[i] = positions[i - 1]  # Set it to be the previous user's position

        previous_score = current_score

    # Get the current user's rank
    user_rank = list(Profile.objects.order_by("-total_score").values_list("total_score", flat=True)).index(
        request.user.profile.total_score) + 1

    # Pass that information to the template
    return render(request, "stats/leaderboard.html",
                  {"top_users": top_users, "positions": positions, "user_rank": user_rank})


# Other Views
def plea_for_no_automated_requests(request):
    logger.warning(f"Someone from the IP address {request.META['REMOTE_ADDR']} is sending too many requests!")
    return HttpResponse("Please do not send requests this fast to the website! You'll make me sad if you do :(",
                        content_type="text/plain")
