"""
commands.py

Created on 2021-01-27
Updated on 2021-01-28

Copyright © Ryan Kan

Description: All the console commands.
"""


# CONSOLE COMMANDS
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
        else:  # JS Implemented command
            output += "\n" + JS_IMPLEMENTED_COMMANDS_HELP[cmd]
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
    "help": help_command
}

JS_IMPLEMENTED_COMMANDS = [
    "clear"
]

JS_IMPLEMENTED_COMMANDS_HELP = {
    "clear": "Clears the console output."
}
