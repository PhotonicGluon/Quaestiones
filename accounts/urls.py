"""
urls.py

Created on 2020-12-27
Updated on 2021-01-11

Copyright © Ryan Kan

Description: The file which contains the URLconf for the `accounts` app.
"""

# IMPORTS
from django.urls import path

from accounts import views

# URL CONFIG
app_name = "accounts"

urlpatterns = [
    path("signup/", views.signup_view, name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("settings/", views.settings_view, name="settings"),
    path("change-password", views.change_password_view, name="change_password"),
    path("change-email", views.change_email_view, name="change_email"),
    path("delete/<username>", views.delete_account_view, name="delete_account"),
    path("activate/<uidb64>/<token>/", views.activate_account_view, name="activate_account"),
    path("confirm-new-email/<uidb64>/<token>/", views.confirm_new_email_view, name="confirm_new_email"),
    path("password-reset/", views.passwordResetView, name="password_reset"),
    path("password-reset/email-sent", views.passwordResetDoneView, name="password_reset_done"),
    path("password-reset/<uidb64>/<token>/", views.passwordResetConfirmView, name="password_reset_confirm"),
    path("password-reset/success", views.passwordResetCompleteView, name="password_reset_complete")
]
