"""
urls.py

Created on 2020-12-26
Updated on 2021-01-01

Copyright © Ryan Kan

Description: The file which contains the URLconfig for the website.
"""

# IMPORTS
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

# URL CONFIG
urlpatterns = [
    path("", include("questions.urls")),
    path("", include("accounts.urls")),
    path("admin/", admin.site.urls)
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
