"""
admin.py

Created on 2020-12-26
Updated on 2020-01-23

Copyright © Ryan Kan

Description: The place to register all the models for easy editing in the admin interface.
"""

# IMPORTS
from django.contrib import admin

from questions.models import Question


# CUSTOM ADMIN INTERFACES
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    fields = ["title", "short_description", "long_description", "input_generation_code", "question_release_datetime",
              "question_input_reset_link"]
    list_display = ["title", "short_description", "pub_date", "last_updated", "id"]
    readonly_fields = ["question_input_reset_link"]
    ordering = ["id"]
