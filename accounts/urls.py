"""
urls.py

Created on 2020-12-27
Updated on 2020-12-30

Copyright © Ryan Kan

Description: The file which contains the URLconf for the `accounts` application.
"""

# IMPORTS
from django.urls import path

from . import views

# URL CONFIG
app_name = "accounts"

urlpatterns = [
    path("signup/", views.signup_view, name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("settings/", views.settings_view, name="settings")
]
