"""
urls.py

Created on 2020-12-26
Updated on 2021-01-24

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
    path("questions/<question_slug>/question", views.display_question, name="display_question"),
    path("questions/<question_slug>/input", views.generate_input, name="generate_input"),
    path("questions/<question_slug>/answer", views.check_question_answer, name="check_question_answer"),

    # Admin-accessible Views
    path("questions/<question_slug>/reset-input-for-all-users", views.reset_question_input,
         name="reset_question_input"),
    path("reset-all-questions-inputs", views.reset_all_question_inputs, name="reset_all_questions_inputs"),
    path("edit-questions/", views.edit_questions_view, name="edit_questions"),
    path("create-question/", views.edit_question_view, name="create_question"),
    path("edit-question/<question_slug>/", views.edit_question_view, name="edit_question"),
    path("preview-question/", views.preview_question_view, name="preview_question"),
    path("delete-question/<question_slug>/", views.delete_question_view, name="delete_question")
]
