"""
urls.py

Created on 2020-02-06
Updated on 2021-02-06

Copyright © Ryan Kan

Description: The file which contains the URLconfig for the `upload_file` application.
"""

# IMPORTS
from django.urls import path

from upload_file import views

# URL CONFIG
urlpatterns = [
    path("upload-file/", views.upload_file_view, name="upload_file")
]
