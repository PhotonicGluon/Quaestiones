"""
get_latest_commit_datetime.py

Created on 2021-01-23
Updated on 2021-02-26

Copyright © Ryan Kan

Description: Gets the latest commit's datetime.
"""

# IMPORTS
import datetime
import os

import git
import pytz
import yaml
from django import template
from git.exc import InvalidGitRepositoryError

from Quaestiones.settings import BASE_DIR, SECRET_FILES_DIR

# SETUP
register = template.Library()


# FUNCTIONS
@register.simple_tag
def get_latest_commit_datetime():
    """
    Gets the string representing the date and time of the latest commit.

    Returns:
        str
    """

    # Get the repository object
    try:
        repo = git.Repo(BASE_DIR)
    except InvalidGitRepositoryError:
        try:
            with open(os.path.join(SECRET_FILES_DIR, "github.yaml"), "r") as f:
                settings = yaml.full_load(f)
            return datetime.datetime.strptime(settings["current-version-datetime"], "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d %H:%M UTC")
        except (KeyError, FileNotFoundError):
            return "Indeterminable"

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
