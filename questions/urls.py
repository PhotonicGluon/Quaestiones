"""
urls.py

Created on 2020-12-26
Updated on 2020-12-26

Copyright © Ryan Kan

Description: The file which contains the URLconfig for the `questions` app.
"""


# IMPORTS
from questions import views
from django.urls import include, path

# URL CONFIG
urlpatterns = [
    path("", views.index, name="index"),
    path("questions/<int:question_id>/", views.display_question, name="display_question")
]
