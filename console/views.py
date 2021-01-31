"""
views.py

Created on 2021-01-27
Updated on 2021-01-31

Copyright © Ryan Kan

Description: The views for the `console` app.
"""

# IMPORTS
import json
import os
import logging

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.middleware.csrf import CsrfViewMiddleware
from django.views.decorators.csrf import csrf_exempt

from console.console import authenticate_user, handle_command_exec
from console.tokens import consoleAccessToken

# CONSTANTS
DEFAULT_DIR = os.getcwd()

# SETUP
logger = logging.getLogger("Quaestiones")


# VIEWS
def console_login_view(request):
    context = {}

    if request.method == "POST":
        # Get the request data
        data = request.POST

        # Get the username and password
        username, password = data["username"], data["password"]

        # Try to authenticate the user
        is_valid = authenticate_user(username, password)

        if is_valid:
            # Generate the token for the user to use the console with
            console_access_token = consoleAccessToken.make_token(request.user)

            # Redirect the user to the actual console page with the token
            return redirect("console:console", token=console_access_token)

        else:
            context = {"failed": True}

    return render(request, "console/login.html", context)


def console_view(request, token=None):
    # Check the validity of the token
    if consoleAccessToken.check_token(request.user, token):
        # Update the current working directory
        os.chdir(DEFAULT_DIR)

        # Render the console page
        return render(request, "console/console.html", {"curr_dir": os.path.abspath(".")})
    else:
        return redirect("console:login")


@csrf_exempt
def execute_command_view(request):
    # Check if a CSRF token was provided
    reason = CsrfViewMiddleware().process_view(request, None, (), {})

    if reason:
        return HttpResponse("CSRF VALIDATION FAILED", content_type="text/plain")

    elif request.method == "POST":
        # Get the post request's data
        data = dict(request.POST)

        # Get the command and its arguments
        command = data["command"][0]
        args = json.loads(data["args"][0])

        # Handle the execution of the command
        output = handle_command_exec(command, args)

        # Handle the response that will be sent to the client
        if output["handle_in_js"]:
            response = "HANDLE IN JS\n"
            response += command + "\n"
            response += json.dumps(args) + "\n"
        elif output["execute_another_in_js"]:
            response = "EXECUTE ANOTHER IN JS\n"
            response += output["output"] + "\n"
            response += json.dumps(output["args"]) + "\n"
        elif output["has_exception"]:
            response = "HAS EXCEPTION\n"
            response += output["output"] + "\n"
        else:
            response = "SUCCESSFULLY EXECUTED\n"
            response += output["output"] + "\n"

        # Output the response
        return HttpResponse(response, content_type="text/plain")
    else:
        return HttpResponse("INVALID METHOD", content_type="text/plain", status=404)
