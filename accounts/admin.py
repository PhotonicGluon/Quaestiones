"""
admin.py

Created on 2020-12-31
Updated on 2020-01-01

Copyright © Ryan Kan

Description: The place to register all the models for easy editing in the admin interface.
"""

# IMPORTS
from django.contrib import admin

from accounts.models import Profile


# CUSTOM ADMIN INTERFACES
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    fields = ["user", "solved_puzzles", "timeout_puzzles"]
    list_display = ["user"]
    readonly_fields = ["user"]
