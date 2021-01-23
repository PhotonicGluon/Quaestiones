"""
urls.py

Created on 2020-12-26
Updated on 2021-01-23

Copyright © Ryan Kan

Description: Django's Command Line Utility for administrative tasks.
"""

# IMPORTS
import logging
import os
import sys


def main():
    # Set the settings
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Quaestiones.settings.development")

    # Get the function that allows Django to execute from the command line
    try:
        from django.core.management import execute_from_command_line

    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and available "
            "on your PYTHONPATH environment variable? Did you forget to activate "
            "a virtual environment? "
        ) from exc

    # Disable logging if it is a test
    if sys.argv[1] == "test":
        logging.disable(logging.CRITICAL)

    # Execute the command from the CLI
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
