"""
admin.py

Created on 2020-12-26
Updated on 2020-12-26

Copyright © Ryan Kan

Description: The place to register all the models for easy editing in the admin interface.
"""

# IMPORTS
from django.contrib import admin
from questions.models import Question

# MODEL REGISTRATION
admin.site.register(Question)
