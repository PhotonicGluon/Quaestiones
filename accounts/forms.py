"""
forms.py

Created on 2021-01-04
Updated on 2021-01-11

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
    email = forms.EmailField(required=True, max_length=200, help_text="Required.", widget=forms.widgets.EmailInput(
        attrs={"required": True, "pattern": "^[A-z0-9._%+-]+@[A-z0-9.-]+\\.[A-z]{2,}$",
               "oninvalid": "this.setCustomValidity(\"Please enter a valid email address.\")",
               "oninput": "this.setCustomValidity(\"\")"}))

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    # Methods
    def clean_email(self):
        """
        This method will be called when the email needs to be cleaned.

        Returns:
            str:
                The cleaned email.

        Raises
            forms.ValidationError:
                If the given email is already registered.
        """

        if User.objects.filter(email=self.cleaned_data["email"]).exists():
            raise forms.ValidationError("The given email is already registered.")
        return self.cleaned_data["email"]


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name"]


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["bio", "theme"]


class ChangeEmailForm(forms.ModelForm):
    email = forms.EmailField(required=True, max_length=200, widget=forms.widgets.EmailInput(
        attrs={"required": True, "pattern": "^[A-z0-9._%+-]+@[A-z0-9.-]+\\.[A-z]{2,}$",
               "oninvalid": "this.setCustomValidity(\"Please enter a valid email address.\")",
               "oninput": "this.setCustomValidity(\"\")"}))

    class Meta:
        model = User
        fields = ["email"]

    # Methods
    def clean_email(self):
        """
        This method will be called when the email needs to be cleaned.

        Returns:
            str:
                The cleaned email.

        Raises
            forms.ValidationError:
                If the given email is already registered.
        """

        if User.objects.filter(email=self.cleaned_data["email"]).exists():
            raise forms.ValidationError("The given email is already registered.")
        return self.cleaned_data["email"]
