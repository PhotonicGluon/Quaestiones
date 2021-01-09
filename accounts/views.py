"""
views.py

Created on 2020-12-27
Updated on 2021-01-08

Copyright © Ryan Kan

Description: The views for the `accounts` application.
"""

# IMPORTS
import logging

from django.contrib.auth import login, logout, views, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils import timezone

from accounts.forms import ProfileForm, EditProfileForm, SignupForm
from accounts.tokens import accountActivationToken

# SETUP
logger = logging.getLogger("Quaestiones")


# VIEWS
def signup_view(request):
    if request.method == "POST":  # Check if it is a POST request
        form = SignupForm(request.POST)  # Pass the data from the POST request

        # Check if the form is valid
        if form.is_valid():
            # Save the user's data to the database
            user = form.save(commit=False)  # Wait until the user has confirmed their email
            user.last_login = timezone.now()  # Update the last login field
            user.is_active = False
            user.save()

            # Send a confirmation email to the user
            current_site = get_current_site(request)
            mail_subject = "Activate Your Quaestiones Account"
            message = render_to_string("accounts/emails/activate_account.html", context={
                "user": user,
                "domain": current_site.domain,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": accountActivationToken.make_token(user),
            })
            to_email = form.cleaned_data.get("email")
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.content_subtype = "html"
            email.send()

            # Report to the log that a user has just signed up
            logger.info(f"A new user '{request.user.get_username()}' just signed up.")

            # Redirect user to the "please confirm your email" page
            return render(request, "accounts/webpages/email_confirmation.html", {"page_type": "confirm email"})

        else:
            logger.info("A person tried to sign up but checks failed.")

    else:  # This is a GET request
        form = SignupForm()  # Define a user creation form

    return render(request, "accounts/webpages/signup.html", {"form": form})  # Send the form to the template


def activate_account(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and accountActivationToken.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return render(request, "accounts/webpages/email_confirmation.html", {"page_type": "success"})
    else:
        return render(request, "accounts/webpages/email_confirmation.html", {"page_type": "invalid token"})


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

    return render(request, "accounts/webpages/login.html", {"form": form})


def logout_view(request):
    if request.method == "GET":  # If the request is a GET request
        logger.info(f"Logging out '{request.user.get_username()}'.")
        logout(request)  # Log the current user out

    return redirect("index")


@login_required(login_url="/login/")
def settings_view(request):
    # Todo: Allow user to edit their email, and then send a confirmation email to their email address
    # Todo: Allow user to delete their account

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
            # Something went wrong; generate the context, and then show the forms page
            context = {"form": form, "profile_form": profile_form}

    else:  # Any other request
        # Get the user's filled-in forms
        form = EditProfileForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)

        # Generate the context
        context = {"form": form, "profile_form": profile_form}

    return render(request, "accounts/webpages/settings.html", context)


def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # This is to prevent the user from logging off
            return render(request, "accounts/webpages/change_password.html", {"page_type": "success"})
        else:
            pass
    else:
        form = PasswordChangeForm(request.user)
    return render(request, "accounts/webpages/change_password.html", {"page_type": "change password", "form": form})


# OTHER VIEWS
# Handle the forgetting of passwords
passwordResetView = views.PasswordResetView.as_view(
    template_name="accounts/webpages/reset_password.html", extra_context={"page_type": "forgot password"},
    success_url=reverse_lazy("accounts:password_reset_done"), email_template_name="accounts/emails/reset_password.html",
    html_email_template_name="accounts/emails/reset_password.html")

passwordResetDoneView = views.PasswordResetDoneView.as_view(
    template_name="accounts/webpages/reset_password.html", extra_context={"page_type": "email sent"})

passwordResetConfirmView = views.PasswordResetConfirmView.as_view(
    template_name="accounts/webpages/reset_password.html", extra_context={"page_type": "reset password"},
    success_url=reverse_lazy("accounts:password_reset_complete"))

passwordResetCompleteView = views.PasswordResetCompleteView.as_view(
    template_name="accounts/webpages/reset_password.html", extra_context={"page_type": "success"})
