"""
commands.py

Created on 2021-01-27
Updated on 2021-01-27

Copyright © Ryan Kan

Description: All the console commands.
"""


# CONSOLE COMMANDS
def echo(*args):
    """
    Echoes whatever is passed into this function.
    """
    return " ".join(args)


def add(a, b):  # Todo: remove this example command
    """
    Adds two numbers together.

    Args:
        a (int):
            The first number.
        b (int):
            The second number.

    Returns:
        int:
            The value of `a + b`.
    """

    return str(int(a) + int(b))


def help_command(cmd=None):
    """
    Help command.

    Args:
        cmd (str):
            Pass in the name of a command to see its corresponding help.
            (Default = None)
    """

    if cmd:
        if cmd in COMMANDS_MAP:
            output = f"Help for `{cmd}`:"
            output += COMMANDS_MAP[cmd].__doc__
        else:  # JS Implemented command
            output = f"JSHelp: {cmd}"
    else:
        output = "**--- Commands ---**\n"
        for command in COMMANDS_MAP.keys():
            output += f"- {command}\n"

        for command in JS_IMPLEMENTED_COMMANDS:
            output += f"- {command}\n"

    return output


# CONSTANTS
COMMANDS_MAP = {
    "echo": echo,
    "add": add,  # Todo: remove this example command
    "help": help_command
}

JS_IMPLEMENTED_COMMANDS = [
    "clear"
]
