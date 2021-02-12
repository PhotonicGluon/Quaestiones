"""
commands.py

Created on 2021-01-27
Updated on 2021-02-13

Copyright © Ryan Kan

Description: All the console commands.
"""

# IMPORTS
import os

from django.contrib.auth.models import User, Permission


# CONSOLE COMMANDS
def add_perm(username, permission):
    """
    Adds the desired permission to the user with the given username.

    Args:
        username (str)

        permission (str):
            Name of the permission to grant the user.
    """

    # Get the desired permission object based on the name of the permission
    if Permission.objects.filter(name=permission).exists():
        permission = Permission.objects.get(name=permission)
    elif Permission.objects.filter(codename=permission).exists():
        permission = Permission.objects.get(codename=permission)
    elif permission == "Is staff member" or permission == "is_staff_member":
        # Will deal with this case separately
        pass
    elif permission == "Is superuser" or permission == "is_superuser":
        # Will deal with this case separately as well
        pass
    else:
        raise ValueError(f"The permission with a name/codename of '{permission}' does not exist.")

    # Get the user with the specified username
    if User.objects.filter(username=username).exists():
        user = User.objects.get(username=username)
    else:
        raise ValueError(f"A user with the username '{username}' does not exist.")

    # Add that permission to the user
    if permission == "Is staff member" or permission == "is_staff_member":
        user.is_staff = True
    elif permission == "Is superuser" or permission == "is_superuser":
        user.is_staff = True
        user.is_superuser = True
    else:
        user.user_permissions.add(permission)

    user.save()

    return "Success!"


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


def mv(curr_path, new_path):
    """
    Moves a file to a new location.

    Args:
        curr_path (str):
            The current path to the file.

        new_path (str):
            The ending path of the file.
    """

    os.rename(curr_path, new_path)

    return ""


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


def remove_perm(username, permission):
    """
    Removes the desired permission from the user with the given username.

    Args:
        username (str)

        permission (str):
            Name of the permission to remove from the user.
    """

    # Get the desired permission object based on the name of the permission
    if Permission.objects.filter(name=permission).exists():
        permission = Permission.objects.get(name=permission)
    elif Permission.objects.filter(codename=permission).exists():
        permission = Permission.objects.get(codename=permission)
    elif permission == "Is staff member" or permission == "is_staff_member":
        # Will deal with this case separately
        pass
    elif permission == "Is superuser" or permission == "is_superuser":
        # Will deal with this case separately as well
        pass
    else:
        raise ValueError(f"The permission with a name/codename of '{permission}' does not exist.")

    # Get the user with the specified username
    if User.objects.filter(username=username).exists():
        user = User.objects.get(username=username)
    else:
        raise ValueError(f"A user with the username '{username}' does not exist.")

    # Remove that permission to the user
    if permission == "Is staff member" or permission == "is_staff_member":
        user.is_staff = False
    elif permission == "Is superuser" or permission == "is_superuser":
        user.is_staff = False
        user.is_superuser = False
    else:
        user.user_permissions.remove(permission)

    user.save()

    return "Success!"


# CONSTANTS
COMMANDS_MAP = {
    "add_perm": add_perm,
    "cd": cd,
    "create_su": create_superuser,
    "echo": echo,
    "help": help_command,
    "ls": ls,
    "mv": mv,
    "remove_perm": remove_perm
}

JS_IMPLEMENTED_COMMANDS = [
    "clear",
    "exit"
]

JS_IMPLEMENTED_COMMANDS_HELP = {
    "clear": "Clears the console output.",
    "exit": "Exits the console."
}
