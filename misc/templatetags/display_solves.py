"""
display_solves.py

Created on 2021-01-25
Updated on 2021-01-25

Copyright © Ryan Kan

Description: Displays the number of solves, if it is to be shown.
"""

# IMPORTS
from django import template

from Quaestiones.settings import ENABLE_SOLVE_STATISTICS

# SETUP
register = template.Library()


# FUNCTIONS
@register.simple_tag
def display_solves(num_solves, force_show_solves=False):
    """
    Properly formats the number of solves to be displayed, if permitted.

    Args:
        num_solves (int)

        force_show_solves (bool):
            Should the number of solves be shown regardless of the value of the `ENABLE_SOLVE_STATISTICS` variable?
            (Default = False)

    Returns:
        str
    """

    if ENABLE_SOLVE_STATISTICS or force_show_solves:
        if num_solves == 1:
            return "[1 Solve]"

        return f"[{num_solves} Solves]"

    return ""
