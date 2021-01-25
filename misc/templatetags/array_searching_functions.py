"""
array_searching_functions.py

Created on 2021-01-25
Updated on 2021-01-25

Copyright © Ryan Kan

Description: Implements array searching functions.
"""

# IMPORTS
from django import template

# SETUP
register = template.Library()


# FUNCTIONS
@register.simple_tag
def get_element_in_index(iterable, i):
    return iterable[i]


@register.simple_tag
def get_index_of_element(iterable, element):
    return iterable.index(element)
