"""
console.py

Created on 2021-01-27
Updated on 2021-01-27

Copyright © Ryan Kan

Description: Handles the incoming console commands.
"""

# IMPORTS
from console.console.commands import COMMANDS_MAP, JS_IMPLEMENTED_COMMANDS


# FUNCTIONS
def handle_command_exec(cmd, args):
    """
    Handles the execution of the command `cmd`.

    Args:
        cmd (str):
            The name of the command.

        *args (list[str]):
            List of arguments to be passed into the command.

    Returns:
        dict:
            The output dictionary.
    """

    # Prepare the output dictionary
    output = {"output": "", "has_exception": False, "handle_in_js": False}

    # Check if the requested command is handled on the javascript side
    if cmd in JS_IMPLEMENTED_COMMANDS:
        output["output"] = cmd
        output["handle_in_js"] = True
    else:
        # Try and find the given command's source function
        try:
            cmd = COMMANDS_MAP[cmd]
        except KeyError:
            output["output"] = f"The command `{cmd}` was not found.\nUse `help` for the list of commands."
        else:
            # Execute the command
            try:
                output["output"] = cmd(*args)
            except Exception as e:
                output["has_exception"] = True
                output["output"] = str(e)

    # Return the output dictionary
    return output


# DEBUG CODE
if __name__ == "__main__":
    result = handle_command_exec("add", ["2", "3"])
    print(result)
    result = handle_command_exec("echo", ["Hello", "World!"])
    print(result)
    result = handle_command_exec("clear", [])
    print(result)
    result = handle_command_exec("not-valid-cmd", ["wow"])
    print(result)
    result = handle_command_exec("help", [])
    print(result)
    result = handle_command_exec("help", ["add"])
    print(result)
    result = handle_command_exec("add", ["2", "3", "1921929021092"])
    print(result)
