"""
commands.py

Created on 2021-01-27
Updated on 2021-01-31

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


def echo(*args):
    """
    Echoes whatever is passed into this function.
    """

    return " ".join(args)


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
        else:  # JS Implemented command
            output += "\n" + JS_IMPLEMENTED_COMMANDS_HELP[cmd]
    else:
        output = "--- Commands ---\n"
        for command in COMMANDS_MAP.keys():
            output += f"- {command}\n"

        for command in JS_IMPLEMENTED_COMMANDS:
            output += f"- {command}\n"

    return output


# CONSTANTS
COMMANDS_MAP = {
    "cd": cd,
    "echo": echo,
    "help": help_command,
    "ls": ls
}

JS_IMPLEMENTED_COMMANDS = [
    "clear"
]

JS_IMPLEMENTED_COMMANDS_HELP = {
    "clear": "Clears the console output."
}
