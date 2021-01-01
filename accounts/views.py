"""
views.py

Created on 2020-12-27
Updated on 2021-01-01

Copyright © Ryan Kan

Description: The views for the `accounts` application.
"""

# IMPORTS
import logging

from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect

# SETUP
logger = logging.getLogger("Quaestiones")


# VIEWS
def signup_view(request):
    if request.method == "POST":  # Check if it is a POST request
        form = UserCreationForm(request.POST)  # Pass the data from the POST request

        # Check if the form is valid
        if form.is_valid():
            # Save the user's data to the database
            user = form.save()

            # Log in the user
            login(request, user)
            logger.info(f"A new user '{request.user.get_username()}' just signed up.")

            # Redirect user to another page
            if "next" in request.POST:
                return redirect(request.POST.get("next"))
            else:
                return redirect("index")

        else:
            logger.info("A person tried to sign up but checks failed.")

    else:  # This is a GET request
        form = UserCreationForm()  # Define a user creation form

    return render(request, "accounts/signup.html", {"form": form})  # Send the form to the template


def login_view(request):
    if request.method == "POST":  # If the request is a POST request
        form = AuthenticationForm(data=request.POST)  # Pass the data from the POST request

        if form.is_valid():
            # Get the user from the form
            user = form.get_user()

            # Log in the user
            login(request, user)
            logger.info(f"The user '{user}' logged in.")

            # Redirect user to another page
            if "next" in request.POST:
                return redirect(request.POST.get("next"))
            else:
                return redirect("index")

        else:
            logger.info(f"Login checks failed for '{request.user.get_username()}'.")

    else:  # GET request
        # Send user a login form and render it
        form = AuthenticationForm()

    return render(request, "accounts/login.html", {"form": form})


def logout_view(request):
    if request.method == "GET":  # If the request is a GET request
        logger.info(f"Logging out '{request.user.get_username()}'.")
        logout(request)  # Log the current user out

    return redirect("index")


def settings_view(request):
    # TODO: Implement settings view
    _ = request
    from django.http import HttpResponse
    return HttpResponse("Not yet implemented")
