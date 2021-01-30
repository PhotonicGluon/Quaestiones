"""
tokens.py

Created on 2021-01-29
Updated on 2021-01-30

Copyright © Ryan Kan

Description: Contains the token generators.
"""

# IMPORTS
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.crypto import constant_time_compare
from django.utils.http import base36_to_int


# CLASSES
class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return str(timestamp * (user.id if user.id else 0 + 1))

    def check_token(self, user, token):
        """
        Check that a password reset token is correct for a given user.
        """
        if not (user and token):
            return False

        # Parse the token
        try:
            ts_b36, _ = token.split("-")
        except ValueError:
            return False

        try:
            ts = base36_to_int(ts_b36)
        except ValueError:
            return False

        # Check that the timestamp/uid has not been tampered with
        if not constant_time_compare(self._make_token_with_timestamp(user, ts), token):
            return False

        # Check the timestamp is within limit.
        if (self._num_seconds(self._now()) - ts) > 10:  # Within 10 minutes
            return False

        return True


# TOKEN GENERATORS
consoleAccessToken = TokenGenerator()
