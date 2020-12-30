"""
urls.py

Created on 2020-12-26
Updated on 2020-12-30

Copyright © Ryan Kan

Description: The file which contains the URLconfig for the `questions` app.
"""


# IMPORTS
from questions import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

# URL CONFIG
urlpatterns = [
    path("", views.index, name="index"),
    path("questions/<int:question_id>/", views.display_question, name="display_question"),
    path("questions/<int:question_id>/input", views.generate_input, name="generate_input"),
    path("questions/<int:question_id>/answer", views.check_question_answer, name="check_question_answer")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
