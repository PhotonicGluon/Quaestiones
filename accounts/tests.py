"""
tests.py

Created on 2020-12-26
Updated on 2021-01-01

Copyright © Ryan Kan

Description: The tests for the `accounts` application.
"""

# IMPORTS
from django.contrib.auth.models import User
from django.test import TestCase, Client


# TESTS
class AccountsTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_signup(self):
        """Tests if the sign up page is working."""

        # Send a signup request to the sign up page
        self.client.post("/signup/", {"username": "TestAccountOne", "password1": "theTestPassword!",
                                      "password2": "theTestPassword!"})

        # Try to get the new user object
        user = User.objects.get(username="TestAccountOne")
        self.assertIsInstance(user, User)

    def test_login(self):
        """Tests if the log in page is working."""

        # Create a fake user object
        User.objects.create_user(username="TestAccountTwo", password="theTestPassword2!")

        # Allow the fake user to log into their account
        response = self.client.post("/login/", {"username": "TestAccountTwo", "password": "theTestPassword2!"})

        # Check if the response code is 302 (Found)
        self.assertEqual(response.status_code, 302)
