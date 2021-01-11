"""
tokens.py

Created on 2021-01-05
Updated on 2021-01-11

Copyright © Ryan Kan

Description: Contains the token generators.
"""

# IMPORTS
from django.contrib.auth.tokens import PasswordResetTokenGenerator


# CLASSES
class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return str(user.pk) + str(timestamp) + str(user.is_active)


# TOKEN GENERATORS
accountActivationToken = TokenGenerator()
newEmailConfirmationToken = TokenGenerator()
