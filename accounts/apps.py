"""
apps.py

Created on 2020-12-27
Updated on 2021-02-01

Copyright © Ryan Kan

Description: The application config for the `accounts` application.
"""

# IMPORTS
import os

from django.apps import AppConfig


# CONFIGURATION
class AccountsConfig(AppConfig):
    name = "accounts"

    def ready(self):
        if not os.getenv("DISABLE_ACCOUNT_DELETION"):
            from accounts.account_deletion_handler import start_account_deletion_job
            start_account_deletion_job()
