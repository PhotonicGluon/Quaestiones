"""
urls.py

Created on 2020-12-26
Updated on 2021-02-10

Copyright © Ryan Kan

Description: The file which contains the URLconfig for the `questions` app.
"""

# IMPORTS
from django.urls import path

from questions import views

# URL CONFIG
app_name = "questions"

urlpatterns = [
    # Main Views
    path("", views.index_view, name="index"),
    path("questions/", views.index_view),
    path("questions/<question_slug>/question", views.display_question_view, name="display-question"),
    path("questions/<question_slug>/input", views.generate_input_view, name="generate-input"),
    path("questions/<question_slug>/answer", views.check_question_answer_view, name="check-question-answer"),

    # Admin-accessible Views
    path("questions/<question_slug>/reset-input-for-all-users", views.reset_question_input_view,
         name="reset-question-input"),
    path("reset-all-questions-inputs", views.reset_all_question_inputs_view, name="reset-all-questions-inputs"),
    path("manage-questions/", views.manage_questions_view, name="manage-questions"),
    path("create-question/", views.edit_question_view, name="create-question"),
    path("edit-question/<question_slug>/", views.edit_question_view, name="edit-question"),
    path("preview-question/", views.preview_question_view, name="preview-question"),
    path("delete-question/<question_slug>/", views.delete_question_view, name="delete-question")
]
