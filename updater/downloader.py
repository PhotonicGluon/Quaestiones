"""
downloader.py

Created on 2021-02-13
Updated on 2021-02-26

Copyright © Ryan Kan

Description: Functions to download files from the GitHub repository.
"""

# IMPORTS
import datetime
import logging
import os
import shutil
import zipfile

import requests
import yaml

from Quaestiones.settings import SECRET_FILES_DIR, BASE_DIR
from updater.file_adder import add
from updater.file_deleter import delete
from updater.github import get_latest_commit_data, check_github_token, check_if_token_is_needed

# SETUP
logger = logging.getLogger("Quaestiones")

# CONSTANTS
THINGS_TO_IGNORE = [
    "Logs",
    "MediaFiles",
    "Other Files",
    "Quaestiones/SecretFiles",
    "Quaestiones/Database.sqlite",
    "Staticfiles"
]


# FUNCTIONS
def check_if_need_update(latest_commit_data, settings):
    """
    Checks if an update is needed.

    Args:
        latest_commit_data (dict):
            The data for the latest commit of Quaestiones.

        settings (dict):
            The settings of the installation of Quaestiones.

    Returns:
        bool:
            Whether an update is needed.

        datetime.datetime:
            What the latest version's release time is.
    """

    # Helper function
    def _parse_commit_datetime(datetime_str):
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

    # Parse the datetimes
    current_version_datetime = _parse_commit_datetime(settings["current-version-datetime"])
    latest_version_datetime = _parse_commit_datetime(latest_commit_data["commit"]["committer"]["date"])

    # Compare the latest commit data's datetime with the current version's datetime
    if current_version_datetime is None or current_version_datetime < latest_version_datetime:
        return True, latest_version_datetime  # Needs update
    return False, latest_version_datetime


def update():
    """
    Performs the update on the current installation of the Quaestiones server.

    Returns:
        bool:
            Whether the update process was successful or not.

    Raises:
        PermissionError:
            If a GitHub token is needed and the provided token is `None` or is invalid.

        FileNotFoundError:
            If the update package was not downloaded properly.
    """

    logging.info("Updater function called. Checking if update is needed.")

    # Update the current working directory
    os.chdir(BASE_DIR)

    # Read the `github.yaml` file and get its contents as a dictionary
    with open(os.path.join(SECRET_FILES_DIR, "github.yaml"), "r") as f:
        settings = yaml.full_load(f)

    # Check if a token is needed to get the data
    if check_if_token_is_needed():
        # Check the token's validity first
        if check_github_token(settings["github-token"]):
            headers = {"Authorization": f"token {settings['github-token']}"}
        else:
            raise PermissionError("The GitHub token is either invalid or is `None` when it is needed.")
    else:
        headers = {}

    # Get the latest commit's data
    latest_commit_data = get_latest_commit_data(headers, commit_type=settings["preferred-version"])

    # Check if an update is needed
    need_update, latest_version_datetime = check_if_need_update(latest_commit_data, settings)
    if not need_update:
        logging.info("You are on the latest version; update not needed.")
        return True  # The update process was successful because nothing had to be updated
    else:
        logging.info("Update available. Starting update process.")

    # An update is needed; get the commit's SHA hash so that we can get the download package
    sha = latest_commit_data["sha"]

    # Generate the download URL
    url = f"https://github.com/Ryan-Kan/Quaestiones/archive/{sha}.zip"

    # Get the request from that URL
    logging.info("Downloading latest version's data.")
    download_request = requests.get(url, headers=headers)
    download_request.raise_for_status()

    # Make a temporary directory to put all the update content in
    os.makedirs("./Update-Package", exist_ok=True)

    # Write the package contents to a ".zip" file
    with open(f"Update-Package/Quaestiones-{sha}.zip", "wb") as f:
        f.write(download_request.content)
    logging.info("Done!")

    # Extract contents of update package
    logging.info("Installing latest version...")

    with zipfile.ZipFile(f"Update-Package/Quaestiones-{sha}.zip", "r") as zip_file:
        zip_file.extractall("Update-Package")
        zip_file.close()

    # Check if update package was downloaded and extracted correctly
    if not os.path.isdir(f"Update-Package/Quaestiones-{sha}"):
        raise FileNotFoundError("Cannot find update package. Abort.")

    # Get the files and folders that cannot be deleted
    cannot_be_deleted = [os.path.abspath(f"Update-Package/Quaestiones-{sha}")] + \
                        [os.path.abspath(x) for x in THINGS_TO_IGNORE]

    # Delete all files and folders in the old directory
    logging.info("Deleting old files.")
    delete(BASE_DIR, cannot_delete=cannot_be_deleted)
    logging.info("Done.")

    # Add update package's contents to the folder
    logging.info("Installing downloaded files.")
    add(os.path.abspath(f"Update-Package/Quaestiones-{sha}"), os.path.abspath("."), cannot_replace=THINGS_TO_IGNORE)
    logging.info("Done.")

    # Delete the update package folder
    shutil.rmtree("./Update-Package")

    # Update the "current-version-datetime" field in the github settings
    settings["current-version-datetime"] = latest_version_datetime.strftime("%Y-%m-%dT%H:%M:%SZ")

    # Update the `github.yaml` file
    with open(os.path.join(SECRET_FILES_DIR, "github.yaml"), "w") as f:
        yaml.dump(settings, f)
        f.close()

    logging.info("Update complete.")
