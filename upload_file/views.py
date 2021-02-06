"""
views.py

Created on 2020-02-06
Updated on 2021-02-06

Copyright © Ryan Kan

Description: The views for the `upload_file` application.
"""

# IMPORTS
import os
import logging

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect

from Quaestiones.settings import UPLOADED_FILES_ROOT, MEDIA_URL
from upload_file.forms import UploadFileForm
from upload_file.handle_file_upload import handle_uploaded_file

# SETUP
logger = logging.getLogger("Quaestiones")


# VIEWS
@staff_member_required(login_url="/login/")
def search_for_file_view(request):
    # Get all the uploaded files
    uploaded_files = os.listdir(UPLOADED_FILES_ROOT)

    # Pass the files list to the `render` function
    return render(request, "upload_file/search_for_file.html", {"uploaded_files_root": UPLOADED_FILES_ROOT, "files": uploaded_files})


@staff_member_required(login_url="/login/")
def upload_file_view(request):
    if request.method == "POST":
        # Fill in the form with the given data
        form = UploadFileForm(request.POST, request.FILES)

        if form.is_valid():
            # Upload the file
            handle_uploaded_file(request.FILES["file"])

            # Show a success alert
            messages.add_message(request, messages.SUCCESS, f"Successfully Uploaded '{request.FILES['file'].name}'.")

            # Redirect to main index page
            return redirect("index")
    else:
        form = UploadFileForm()

    return render(request, "upload_file/upload_file.html", {"form": form})
