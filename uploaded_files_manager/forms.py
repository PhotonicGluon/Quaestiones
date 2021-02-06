"""
forms.py

Created on 2021-02-06
Updated on 2021-02-06

Copyright © Ryan Kan

Description: The forms for the `uploaded_files_manager` application.
"""

# IMPORTS
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from accounts.models import Profile


# CLASSES
class UploadFileForm(forms.Form):
    file = forms.FileField(help_text="Make sure the file has been named appropriately.")
