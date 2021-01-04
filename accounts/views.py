"""
views.py

Created on 2020-12-27
Updated on 2021-01-04

Copyright © Ryan Kan

Description: The views for the `accounts` application.
"""

# IMPORTS
import logging

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect

from accounts.forms import ProfileForm, EditProfileForm

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


@login_required(login_url="/login/")
def settings_view(request):
    if request.method == "POST":
        # Get the forms
        form = EditProfileForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)

        # Check if both forms are okay
        if form.is_valid() and profile_form.is_valid():
            # If so, save both forms
            user_form = form.save()
            custom_form = profile_form.save(False)
            custom_form.user = user_form
            custom_form.save()

            # Redirect to the main page
            return redirect("index")
    else:
        # Show the user's forms
        form = EditProfileForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)

        # Render the page
        context = {"form": form, "profile_form": profile_form}
        return render(request, "accounts/settings.html", context)
