"""
file_adder.py

Created on 2021-02-26
Updated on 2021-02-26

Copyright © Ryan Kan

Description: Adds a file to the correct directory.
"""

# IMPORTS
import os
import shutil


# FUNCTIONS
def add_file(orig_path, dest_path, cannot_replace_files=None):
    """
    Adds the file at the original path at the destination.

    Args:
        orig_path (str):
            The file's original path.

        dest_path (str):
            Where the file should be added to.

        cannot_replace_files (optional[list[str]]):
            List of absolute paths of files that cannot be replaced.

    Returns:
        bool:
            Whether the file was added or not.
    """

    # If `cannot_replace_files` is `None`, then replace it with an empty list
    if cannot_replace_files is None:
        cannot_replace_files = []

    if dest_path in cannot_replace_files:
        return False
    else:
        shutil.copy(orig_path, dest_path)
        return True


def add(src, dest, cannot_replace=None):
    """
    Recursively adds files from the source to the destination.

    Args:
        src (str):
            Original file/folder location.

        dest (str):
            Destination of the new file/folder.

        cannot_replace (optional[list[str]]):
            List of absolute paths of files that cannot be replaced.

    Returns:
        bool:
            Whether the file was added or not.
    """

    # If `cannot_replace` is `None`, then replace it with an empty list
    if cannot_replace is None:
        cannot_replace = []

    # Determine if the source exists
    src = os.path.abspath(src)

    if not os.path.exists(src):
        return False  # There is no file that can be added

    # Make the destination folder if the destination folder does not exist
    dest = os.path.abspath(dest)
    os.makedirs(dest, exist_ok=True)

    # Determine what type of 'thing' is at the source path
    if os.path.isfile(src):
        return add_file(src, dest, cannot_replace_files=cannot_replace)
    else:  # It is a folder
        # Check if the destination directory itself is in the `cannot_replace` list
        if dest in cannot_replace:
            return False
        else:
            # Add all files/folders in the source directory
            all_files = os.listdir(src)

            for file in all_files:
                if os.path.isdir(os.path.join(src, file)):
                    add(os.path.join(src, file), os.path.join(dest, file), cannot_replace=cannot_replace)
                else:
                    add_file(os.path.join(src, file), os.path.join(dest, file), cannot_replace_files=cannot_replace)

            return True
