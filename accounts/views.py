"""
views.py

Created on 2020-12-27
Updated on 2021-01-11

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
from django.utils import timezone
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from accounts.forms import ProfileForm, EditProfileForm, SignupForm, ChangeEmailForm
from accounts.tokens import accountActivationToken, newEmailConfirmationToken

# SETUP
logger = logging.getLogger("Quaestiones")


# VIEWS
def signup_view(request):
    # Todo: allow user to resend confirmation email

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
            return render(request, "accounts/webpages/account_activation.html", {"page_type": "confirm email"})

        else:
            logger.info("A person tried to sign up but checks failed.")

    else:  # This is a GET request
        form = SignupForm()  # Define a user creation form

    return render(request, "accounts/webpages/signup.html", {"form": form})  # Send the form to the template


def activate_account_view(request, uidb64, token):
    # Try to get the user who requested for the activation of the account
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))  # The user's id
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    # Check if the activation token is valid
    if user is not None and accountActivationToken.check_token(user, token):
        # Activate the account
        user.is_active = True
        user.save()

        # Log in the user
        login(request, user)

        # Tell the user that the activation was a success
        context = {"page_type": "success"}

    else:
        context = {"page_type": "invalid token"}

    return render(request, "accounts/webpages/account_activation.html", context)


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
    # Form the regex for the deletion command
    regex_for_deletion = "".join([f"[{char.lower()}{char.upper()}]" for char in request.user.username])

    # Handle the request
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
            context = {"form": form, "profile_form": profile_form, "regex_for_deletion": regex_for_deletion}

    else:  # Any other request
        # Get the user's filled-in forms
        form = EditProfileForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)

        # Generate the context
        context = {"form": form, "profile_form": profile_form, "regex_for_deletion": regex_for_deletion}

    return render(request, "accounts/webpages/settings.html", context)


@login_required(login_url="/login/")
def change_password(request):
    if request.method == "POST":
        # Get the form
        form = PasswordChangeForm(request.user, request.POST)

        # Check if the password change form is valid
        if form.is_valid():
            # Then update the user's password and their session's hash
            user = form.save()
            update_session_auth_hash(request, user)  # This is to prevent the user from logging off

            # Show the resulting webpage to the user
            return render(request, "accounts/webpages/change_password.html", {"page_type": "success"})

    else:
        # Show the EMPTY password change form to the user
        form = PasswordChangeForm(request.user)

    # Show the resulting webpage to the user
    return render(request, "accounts/webpages/change_password.html", {"page_type": "change password", "form": form})


@login_required(login_url="/login/")
def change_email_view(request):
    # Todo: allow user to resend confirmation email
    if request.method == "POST":
        # Get the filled in form
        form = ChangeEmailForm(request.POST, instance=request.user)

        # Check if the email change form is valid
        if form.is_valid():
            # Save this possible new email to the user's profile object
            to_email = form.cleaned_data.get("email")
            request.user.profile.possible_new_email = to_email
            request.user.profile.save()

            # Send an email to the new address
            current_site = get_current_site(request)
            mail_subject = "New Email Address Confirmation"
            message = render_to_string("accounts/emails/change_email.html", context={
                "user": request.user,
                "domain": current_site.domain,
                "uid": urlsafe_base64_encode(force_bytes(request.user.pk)),
                "token": newEmailConfirmationToken.make_token(request.user)
            })
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.content_subtype = "html"
            email.send()

            # Show the resulting webpage to the user
            return render(request, "accounts/webpages/change_email.html", {"page_type": "confirm email"})
    else:
        # Show the EMPTY email change form to the user
        form = ChangeEmailForm()

    # Show the resulting webpage to the user
    return render(request, "accounts/webpages/change_email.html", {"page_type": "change email", "form": form})


def confirm_new_email_view(request, uidb64, token):
    # Try to get the user who requested for the activation of the account
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))  # The user's id
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    # Check if the token is valid
    if user is not None and newEmailConfirmationToken.check_token(user, token):
        # Change the email address
        user.email = user.profile.possible_new_email
        user.profile.possible_new_email = user.profile.possible_new_email

        user.save()
        user.profile.save()

        # Generate the context
        context = {"page_type": "success", "email": user.email}

    else:
        context = {"page_type": "invalid token"}

    return render(request, "accounts/webpages/change_email.html", context)


@login_required(login_url="/login/")
def delete_account_view(request, username):
    if request.method == "POST":  # This is coming from the settings page
        # Get the user that requested the deletion
        user = User.objects.get(username=username)

        # Set the user to be "not active"
        user.is_active = False
        user.save()

        # Log out the user
        logout(request)

        # Report the deletion to the logs
        logger.info(f"'{username}' has just scheduled their account for deletion.")

        # Send an email to the user
        mail_subject = "Your Quaestiones Account Was Deleted"
        message = render_to_string("accounts/emails/delete_account.html", context={"user": user})
        to_email = user.email
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.content_subtype = "html"
        email.send()

        # Show the account deletion confirmation page
        return render(request, "accounts/webpages/delete_account.html")

    # If not, then this was an invalid request; show the index page
    return redirect("index")


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
