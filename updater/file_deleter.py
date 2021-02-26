"""
file_deleter.py

Created on 2021-02-20
Updated on 2021-02-20

Copyright © Ryan Kan

Description: Handles the deletion of files and folders.
"""

# IMPORTS
import os


# FUNCTIONS
def delete_file(file_path, cannot_delete_files=None):
    """
    Deletes the file at the `file_path`.

    Args:
        file_path (str)

        cannot_delete_files (optional[list[str]]):
            List of absolute paths of files that cannot be deleted.

    Returns:
        bool:
            Whether the file was deleted or not.
    """

    # If `cannot_delete_files` is `None`, then replace it with an empty list
    if cannot_delete_files is None:
        cannot_delete_files = []

    if file_path in cannot_delete_files:
        return False
    else:
        os.remove(file_path)
        return True


def delete(path, cannot_delete=None):
    """
    Recursively delete files in a path, unless if it cannot be deleted.

    Args:
        path (str):
            Path to a directory or file.

        cannot_delete (optional[list[str]]):
            List of absolute paths of files or folders that cannot be deleted.

    Returns:
        bool:
            Whether the file was deleted or not.
    """

    # If `cannot_delete` is `None`, then replace it with an empty list
    if cannot_delete is None:
        cannot_delete = []

    # Determine if the file actually exists
    path = os.path.abspath(path)

    if not os.path.exists(path):
        return False  # There is no file to be deleted

    # Determine what type of 'thing' is at the path
    if os.path.isfile(path):
        return delete_file(path, cannot_delete_files=cannot_delete)
    else:  # It is a folder
        # Check if the directory itself is in the `cannot_delete` list
        if path in cannot_delete:
            return False
        else:
            # Delete all files in the folder
            all_files = os.listdir(path)

            for file in all_files:
                file = os.path.join(path, file)

                if os.path.isdir(file):
                    delete(file, cannot_delete=cannot_delete)
                else:
                    delete_file(file, cannot_delete_files=cannot_delete)

            # Now delete the folder itself
            try:
                os.rmdir(path)
            except OSError:
                pass

            return True
