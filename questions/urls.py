"""
urls.py

Created on 2020-12-26
Updated on 2021-01-23

Copyright © Ryan Kan

Description: The file which contains the URLconfig for the `questions` app.
"""

# IMPORTS
from django.urls import path

from questions import views

# URL CONFIG
urlpatterns = [
    # Main Views
    path("", views.index, name="index"),
    path("questions/", views.index),
    path("questions/<int:question_id>/", views.display_question, name="display_question"),
    path("questions/<int:question_id>/OK=<override_key>/", views.display_question, name="display_question"),
    path("questions/<int:question_id>/input", views.generate_input, name="generate_input"),
    path("questions/<int:question_id>/answer", views.check_question_answer, name="check_question_answer"),

    # Admin-accessible Views
    path("questions/<int:question_id>/reset-input-for-all-users", views.reset_question_input,
         name="reset_question_input"),
    path("edit-questions/", views.edit_questions_view, name="edit_questions"),
    path("create-question/", views.edit_question_view, name="create_question"),
    path("edit-question/<question_id>", views.edit_question_view, name="edit_question"),
    path("preview-question/", views.preview_question_view, name="preview_question"),
    path("delete-question/<question_id>", views.delete_question_view, name="delete_question")
]
