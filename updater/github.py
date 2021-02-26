"""
github.py

Created on 2021-02-13
Updated on 2021-02-20

Copyright © Ryan Kan

Description: GitHub functions.
"""

# IMPORTS
import json

import requests
import yaml


# FUNCTIONS
def get_latest_commit_data(headers, commit_type="stable"):
    """
    Gets the latest commit's data from the GitHub API, given the type of commit that is desired.

    Args:
        headers (dict):
            The headers to be sent along the request to get the latest commit data.

        commit_type (str):
            Must be one of ["release", "stable", "development"].
            - "release"     means the latest release version's latest commit.
            - "stable"      means the latest stable build on the "main" branch.
            - "development" means the latest build on the "Development" branch.
            (Default = "stable")

    Returns:
        dict:
            The latest commit's information.

    Raises:
        AssertionError:
            If the `url_type` is NOT one of ["release", "stable", "development"].

        FileNotFoundError:
            If there are no releases available.
    """

    # Perform sanity-check on the url type
    assert commit_type.lower() in ["release", "stable", "development"], \
        "The `commit_type` must be one of [\"release\", \"stable\", \"development\"]."

    # Handle each URL type separately
    if commit_type == "release":
        # Get the tags of all the releases
        response = requests.get("https://api.github.com/repos/Ryan-Kan/Quaestiones/tags", headers=headers)
        response.raise_for_status()

        # Load the response as a JSON object
        tags = json.loads(response.text)

        # Check if there are releases
        if len(tags) == 0:
            # Then there are no releases; raise a `FileNotFound` error
            raise FileNotFoundError("There are no releases available.")
        else:
            # Then the first one is the most recent one; get its commit url
            commit_url = tags[0]["commit"]["url"]

    else:  # The other two have similar processes of getting the commit url
        # Get the correct API url
        if commit_type == "stable":
            api_url = "https://api.github.com/repos/Ryan-Kan/Quaestiones/branches/main"
        else:
            api_url = "https://api.github.com/repos/Ryan-Kan/Quaestiones/branches/Development"

        # Query the GitHub API to get the latest commit
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()

        # Get the commit url from the returned JSON data
        data = json.loads(response.text)
        commit_url = data["commit"]["url"]

    # Get the commit's data
    response = requests.get(commit_url, headers=headers)
    response.raise_for_status()
    return json.loads(response.text)


def check_if_token_is_needed():
    """
    Checks if an access token is needed to access the github repository.

    Returns:
        bool
    """

    request = requests.get("https://api.github.com/repos/Ryan-Kan/Quaestiones/branches/main")

    try:
        request.raise_for_status()
        return False

    except requests.HTTPError:
        return True


def get_github_token(secrets_file):
    """
    Gets the github access token from the secrets' file.

    Args:
        secrets_file (str):
            Path to the secrets file.

    Returns:
        union[str, None]: The github access token. Returns `None` if not found.
    """

    token = None
    with open(secrets_file, "r") as f:
        file_contents = yaml.full_load(f)

        if "github-token" in file_contents.keys():
            token = file_contents["github-token"]

    return token


def check_github_token(token):
    """
    Checks whether the given is correct or not.

    Args:
        token (Optional[str]):
            The github access token.

    Returns:
        bool: Whether the token is correct or not.
    """

    # Check if token is None
    if token is None:
        return False

    # Form header
    header = {"Authorization": f"token {token}"}

    request = requests.get("https://api.github.com/repos/Ryan-Kan/Quaestiones/branches/main", headers=header)

    # Check if got response
    try:
        request.raise_for_status()
        return True

    except requests.HTTPError:
        return False


# DEBUG CODE
if __name__ == "__main__":
    t = get_github_token("../Quaestiones/SecretFiles/github.yaml")
    print(t)
    print(get_latest_commit_data({"Authorization": f"token {t}"}))
