"""
forms.py

Created on 2021-01-04
Updated on 2021-01-04

Copyright © Ryan Kan

Description: The forms for the `accounts` application.
"""

# IMPORTS
from django.contrib.auth.models import User
from django.forms import ModelForm

from accounts.models import Profile


# CLASSES
class EditProfileForm(ModelForm):
    class Meta:
        model = User
        fields = ["email", "first_name", "last_name"]


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ["bio"]
