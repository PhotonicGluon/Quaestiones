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

    # Assert that the current working directory is the root directory
    assert os.path.basename(os.getcwd()) == "Quaestiones", "The current working directory was improperly set."

    # Run the authenticator program
    pipe_open = Popen(["console/console/authenticator"], stdout=PIPE, stdin=PIPE)
    pipe_open.stdin.write(bytes(f"{username}\n{password}\n", "UTF-8"))
    pipe_open.stdin.flush()

    output = pipe_open.stdout.readline().strip()

    # Return the output as a boolean
    return True if output == b"1" else False


# DEBUG CODE
if __name__ == "__main__":
    os.chdir("../..")

    u = input("Username: ")
    p = input("Password: ")

    print(authenticate_user(u, p))
