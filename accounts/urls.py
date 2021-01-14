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
    path("change-password", views.change_password_view, name="change_password"),
    path("change-email", views.change_email_view, name="change_email"),
    path("delete/<username>", views.delete_account_view, name="delete_account"),

    # Views that require a token
    path("activate/<uidb64>/<token>/", views.activate_account_view, name="activate_account"),
    path("confirm-new-email/<uidb64>/<token>/", views.confirm_new_email_view, name="confirm_new_email"),

    # Email Sending Views
    path("send-email/activate-account", views.send_activate_account_email_view, name="send_activate_account_email"),
    path("send-email/confirm-new-email-address", views.send_confirm_new_email_address_email_view,
         name="send_confirm_new_email_address_email"),

    # Password Reset Views
    path("password-reset/", views.passwordResetView, name="password_reset"),
    path("password-reset/email-sent", views.passwordResetDoneView, name="password_reset_done"),
    path("password-reset/<uidb64>/<token>/", views.passwordResetConfirmView, name="password_reset_confirm"),
    path("password-reset/success", views.passwordResetCompleteView, name="password_reset_complete")
]
