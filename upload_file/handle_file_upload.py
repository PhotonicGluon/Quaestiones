"""
handle_file_upload.py

Created on 2021-02-06
Updated on 2021-02-06

Copyright © Ryan Kan

Description: Handles the uploading of files.
"""

# IMPORTS
import os

from Quaestiones.settings import UPLOADED_FILES_ROOT


# FUNCTIONS
def handle_uploaded_file(f):
    """
    Handles the uploaded file.

    Args:
        f (UploadedFile)
    """

    with open(os.path.join(UPLOADED_FILES_ROOT, f.name), "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)
