"""
urls.py

Created on 2020-12-26
Updated on 2020-12-31

Copyright © Ryan Kan

Description: The file which contains the URLconfig for the `questions` app.
"""


# IMPORTS
from questions import views
from django.urls import path

# URL CONFIG
urlpatterns = [
    path("", views.index, name="index"),
    path("questions/<int:question_id>/", views.display_question, name="display_question"),
    path("questions/<int:question_id>/input", views.generate_input, name="generate_input"),
    path("questions/<int:question_id>/answer", views.check_question_answer, name="check_question_answer")
]
