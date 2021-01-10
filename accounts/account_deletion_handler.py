"""
account_deletion_handler.py

Created on 2021-01-08
Updated on 2021-01-10

Copyright © Ryan Kan

Description: Handles the automatic deletion of inactive accounts.
"""

# IMPORTS
import logging
import os
import shutil
from datetime import timedelta

from apscheduler.schedulers.background import BackgroundScheduler
from django.contrib.auth.models import User
from django.utils import timezone

from Quaestiones.settings.common import DAYS_INACTIVE_BEFORE_DELETE, MEDIA_ROOT

# SETUP
logger = logging.getLogger("Quaestiones")


# FUNCTIONS
def get_inactive_accounts():
    """
    Gets the set of the inactive accounts in the database.

    Returns:
        QuerySet:
            The queryset of user accounts that are inactive.
    """

    return User.objects.filter(is_active=False)


def get_deletable_accounts():
    """
    Gets the set of deletable accounts in the database.

    Returns:
        QuerySet[User]:
            The queryset of user accounts that can be deleted.
    """

    # Get the inactive accounts
    inactive_accounts = get_inactive_accounts()

    # Get the current datetime
    current_datetime = timezone.now()

    # Get the datetime that is `DAYS_INACTIVE_BEFORE_DELETE` days before
    past_datetime = current_datetime - timedelta(days=DAYS_INACTIVE_BEFORE_DELETE)

    # Only get the accounts that are inactive and that login earlier than the `past_datetime`
    deletable_accounts = inactive_accounts.filter(last_login__lte=past_datetime)

    # Return that set of accounts
    return deletable_accounts


def delete_inactive_accounts():
    """
    Deletes the deletable accounts from the database.
    """

    # Get the deletable accounts
    deletable_accounts = get_deletable_accounts()

    # Check if there are objects to be deleted
    if deletable_accounts.count() > 0:
        # Get the usernames of the deleted accounts
        deleted_accounts_usernames = list(deletable_accounts.values_list('username', flat=True))

        # Report the accounts that will be deleted to the log
        logger.info(f"Deleted {', '.join(deleted_accounts_usernames)} because they were inactive for too long.")

        # Delete all those accounts
        deletable_accounts.delete()

        # Delete those accounts' media folders as well
        for username in deleted_accounts_usernames:
            try:
                shutil.rmtree(os.path.join(MEDIA_ROOT, f"{username}"))
            except FileNotFoundError:
                pass

    else:
        # Report that there are no accounts to be deleted
        logger.info(f"There were no accounts to delete.")


def start_account_deletion_job():
    """
    Starts the automated accounts deletion job.
    """

    # Run the deletion process initially
    delete_inactive_accounts()

    # Schedule it to run every day
    scheduler = BackgroundScheduler()  # Makes a separate thread to run the deletion process
    scheduler.add_job(delete_inactive_accounts, "interval", days=1)  # Runs the deletion process every 1 day
    scheduler.start()
