"""
urls.py

Created on 2020-12-26
Updated on 2020-12-26

Copyright © Ryan Kan

Description: The file which contains the URLconfig for the website.
"""


# IMPORTS
from django.contrib import admin
from django.urls import include, path

# URL CONFIG
urlpatterns = [
    path("", include("questions.urls")),
    path("auth/", include("accounts.urls")),
    path("admin/", admin.site.urls)
]
