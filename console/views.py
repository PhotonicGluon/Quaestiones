"""
views.py

Created on 2021-01-27
Updated on 2021-01-27

Copyright © Ryan Kan

Description: The views for the `console` app.
"""

# IMPORTS
import json
import logging

from django.http import HttpResponse
from django.shortcuts import render

from console.console import handle_command_exec

# SETUP
logger = logging.getLogger("Quaestiones")


# VIEWS
def console_view(request):
    return render(request, "console/console.html")


def execute_command_view(request):
    if request.method == "POST":
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
        elif output["has_exception"]:
            response = "HAS EXCEPTION\n"
            response += output["output"] + "\n"
        else:
            response = "SUCCESSFULLY EXECUTED\n"
            response += output["output"] + "\n"

        # Output the response
        return HttpResponse(response)
    else:
        return HttpResponse("INVALID METHOD")
