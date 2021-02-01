"""
authentication.py

Created on 2021-01-28
Updated on 2021-02-01

Copyright © Ryan Kan

Description: Functions to handle the logging in of superusers to the console.
"""

# IMPORTS
import os
from subprocess import Popen, PIPE

from Quaestiones.settings.common import BASE_DIR


# FUNCTIONS
def authenticate_user(username, password):
    """
    Authenticates the user to the console backend.

    Args:
        username (str):
            Username or Console Override Code (COC).

        password (str)

    Returns:
        bool:
            Whether the user is valid or not.
    """

    # Set the current working directory to the root directory
    os.chdir(BASE_DIR)

    # Run the authenticator program
    pipe_open = Popen(["console/console/authenticator"], stdout=PIPE, stdin=PIPE)
    pipe_open.stdin.write(bytes(f"{username}\n{password}\n", "UTF-8"))
    pipe_open.stdin.flush()

    output = pipe_open.stdout.readline().strip()

    # Return the output as a boolean
    return True if output == b"1" else False


# DEBUG CODE
if __name__ == "__main__":
    print(authenticate_user(input("Username: "), input("Password: ")))
