"""
commands.py

Created on 2021-01-27
Updated on 2021-02-02

Copyright © Ryan Kan

Description: All the console commands.
"""

# IMPORTS
import os


# CONSOLE COMMANDS
def cd(dir_path):
    """
    Navigates to the specified path.

    Args:
        dir_path (str):
            Relative path to take to get to the new directory.
    """

    # Navigate to the new directory
    os.chdir(os.path.join(os.path.curdir, dir_path))

    # Return the output
    return "cd", [os.path.abspath(os.getcwd())], True  # To also be executed in JS


def create_superuser(username, email, password):
    """
    Creates a new superuser based on the given username, email and password.

    Args:
        username (str)
        email (str)
        password (str)

    Returns:
        str:
            Whether the operation was successful.
    """

    from django.contrib.auth import get_user_model
    user = get_user_model()
    user.objects.create_superuser(username, email, password)

    return "Success!"


def echo(*args):
    """
    Echoes whatever is passed into this function.
    """

    return " ".join(args)


def help_command(cmd=None):
    """
    Help command.

    Args:
        cmd (str):
            Pass in the name of a command to see its corresponding help.
            (Default = None)
    """

    if cmd:
        output = f"Help for `{cmd}`:"

        if cmd in COMMANDS_MAP:
            output += COMMANDS_MAP[cmd].__doc__
        elif cmd in JS_IMPLEMENTED_COMMANDS:  # JS Implemented command
            output += "\n    " + JS_IMPLEMENTED_COMMANDS_HELP[cmd]
        else:
            output = f"There is no command called `{cmd}`."
    else:
        output = "--- Commands ---\n"
        commands = sorted(list(COMMANDS_MAP.keys()) + JS_IMPLEMENTED_COMMANDS)

        for command in commands:
            output += f"- {command}\n"

    return output


def ls(dir_path="."):
    """
    List directory contents.

    Args:
        dir_path (str):
            Path to the directory.
            (Default = ".")
    """

    files = os.listdir(dir_path)

    output = ""
    for file in files:
        output += f"- {file}\n"

    return output


# CONSTANTS
COMMANDS_MAP = {
    "cd": cd,
    "create_su": create_superuser,
    "echo": echo,
    "help": help_command,
    "ls": ls
}

JS_IMPLEMENTED_COMMANDS = [
    "clear",
    "exit"
]

JS_IMPLEMENTED_COMMANDS_HELP = {
    "clear": "Clears the console output.",
    "exit": "Exits the console."
}
