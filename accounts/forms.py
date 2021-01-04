"""
forms.py

Created on 2021-01-04
Updated on 2021-01-05

Copyright © Ryan Kan

Description: The forms for the `accounts` application.
"""

from django import forms
# IMPORTS
from django.contrib.auth.models import User

from accounts.models import Profile


# CLASSES
class EditProfileForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.widgets.EmailInput(
        attrs={"required": True, "pattern": "^[A-z0-9._%+-]+@[A-z0-9.-]+\\.[A-z]{2,}$",
               "oninvalid": "this.setCustomValidity(\"Please enter a valid email addess.\")",
               "oninput": "this.setCustomValidity(\"\")"}))

    class Meta:
        model = User
        fields = ["email", "first_name", "last_name"]


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["bio"]
