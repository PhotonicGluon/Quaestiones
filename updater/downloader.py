"""
downloader.py

Created on 2021-02-13
Updated on 2021-02-16

Copyright © Ryan Kan

Description: Functions to download files from the GitHub repository.
"""

# IMPORTS
import datetime
import json
import logging
import os
import re
import zipfile
from shutil import copy, copytree, rmtree

import requests
import yaml

from Quaestiones.settings import SECRET_FILES_DIR
from updater.github import get_latest_commit_data, get_github_token, check_github_token, check_if_token_is_needed

# CONSTANTS
THINGS_TO_IGNORE = []


# FUNCTIONS
def parse_commit_datetime(datetime_str):
    """
    Parses the datetime string as a valid datetime object.

    Args:
        datetime_str (str)

    Returns:
        union[datetime.datetime, None]:
            Returns a datetime object, unless it is invalid in which case a `None` is returned instead.
    """

    try:
        return datetime.datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%SZ")
    except ValueError:
        return None


def check_if_need_update(latest_commit_data):
    """
    Checks if an update is needed.

    Args:
        latest_commit_data (dict):
            The data for the latest commit of Quaestiones.

    Returns:
        bool
    """

    # Read the `github.yaml` file and get its contents as a dictionary
    with open(os.path.join(SECRET_FILES_DIR, "github.yaml"), "r") as f:
        settings = yaml.full_load(f)

    # Parse the datetimes
    current_version_datetime = parse_commit_datetime(settings["current-version-datetime"])
    latest_version_datetime = parse_commit_datetime(latest_commit_data["commit"]["committer"]["date"])

    # Compare the latest commit data's datetime with the current version's datetime
    if current_version_datetime < latest_version_datetime:
        return True  # Needs update
    return False


def update():
    """
    Performs the update on the current installation of the Quaestiones server.
    """
    # Todo: Fill in


# DEBUG CODE
if __name__ == "__main__":
    check_if_need_update(get_latest_commit_data(token=get_github_token(os.path.join(SECRET_FILES_DIR, "github.yaml"))))
