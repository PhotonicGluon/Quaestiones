"""
get_latest_commit_datetime.py

Created on 2021-01-23
Updated on 2021-01-23

Copyright © Ryan Kan

Description: Gets the latest commit's datetime.
"""

# IMPORTS
import pytz
from django import template
import git

from Quaestiones.settings import BASE_DIR


# SETUP
register = template.Library()


# FUNCTIONS
@register.simple_tag
def get_latest_commit_datetime():
    """
    Gets the datetime object representing the date of the latest commit.

    Returns:
        datetime.datetime
    """

    # Get the repository object
    repo = git.Repo(BASE_DIR)

    # Get the most recent commit
    most_recent_commit = repo.head.commit

    # Get the datetime of that commit
    commit_datetime = most_recent_commit.committed_datetime

    # Convert the local datetime to the UTC datetime
    commit_datetime = commit_datetime.astimezone(pytz.utc)

    # Format the datetime object
    output_string = commit_datetime.strftime("%Y-%m-%d %H:%M UTC")

    return output_string


# DEBUG CODE
if __name__ == "__main__":
    print(get_latest_commit_datetime())
