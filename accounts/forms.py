"""
forms.py

Created on 2021-01-04
Updated on 2021-01-05

Copyright © Ryan Kan

Description: The forms for the `accounts` application.
"""

# IMPORTS
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from accounts.models import Profile


# CLASSES
class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text="Required.", widget=forms.widgets.EmailInput(
        attrs={"required": True, "pattern": "^[A-z0-9._%+-]+@[A-z0-9.-]+\\.[A-z]{2,}$",
               "oninvalid": "this.setCustomValidity(\"Please enter a valid email address.\")",
               "oninput": "this.setCustomValidity(\"\")"}))

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name"]  # Todo: allow user to edit their email, and then send a confirmation email


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["bio"]
