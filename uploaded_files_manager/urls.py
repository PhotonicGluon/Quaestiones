"""
urls.py

Created on 2020-02-06
Updated on 2021-02-10

Copyright © Ryan Kan

Description: The file which contains the URLconfig for the `uploaded_files_manager` application.
"""

# IMPORTS
from django.urls import path

from uploaded_files_manager import views

# URL CONFIG
app_name = "uploaded_files_manager"

urlpatterns = [
    path("manage-files/", views.manage_files_view, name="manage-files"),
    path("upload-file/", views.upload_file_view, name="upload_file"),
    path("delete-file", views.delete_file_view, name="delete_file")
]
