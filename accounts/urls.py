"""
urls.py

Created on 2020-12-27
Updated on 2021-01-14

Copyright © Ryan Kan

Description: The file which contains the URLconf for the `accounts` app.
"""

# IMPORTS
from django.urls import path

from accounts import views

# URL CONFIG
app_name = "accounts"

urlpatterns = [
    # Signup, Login and Logout Views
    path("signup/", views.signup_view, name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    # Settings Related Views
    path("settings/", views.settings_view, name="settings"),
    path("change-password", views.change_password_view, name="change-password"),
    path("change-email", views.change_email_view, name="change-email"),
    path("delete/<username>", views.delete_account_view, name="delete-account"),

    # Views that require a token
    path("activate/<uidb64>/<token>/", views.activate_account_view, name="activate-account"),
    path("confirm-new-email/<uidb64>/<token>/", views.confirm_new_email_view, name="confirm-new-email"),

    # Email Sending Views
    path("send-email/activate-account", views.send_activate_account_email_view, name="send-activate-account-email"),
    path("send-email/confirm-new-email-address", views.send_confirm_new_email_address_email_view,
         name="send-confirm-new-email-address-email"),

    # Password Reset Views
    path("password-reset/", views.passwordResetView, name="password-reset"),
    path("password-reset/email-sent", views.passwordResetDoneView, name="password-reset-done"),
    path("password-reset/<uidb64>/<token>/", views.passwordResetConfirmView, name="password-reset-confirm"),
    path("password-reset/success", views.passwordResetCompleteView, name="password-reset-complete")
]
