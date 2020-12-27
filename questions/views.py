"""
views.py

Created on 2020-12-26
Updated on 2020-12-26

Copyright © Ryan Kan

Description: The views for the `questions` app.
"""

# IMPORTS
from django.shortcuts import render, get_object_or_404

from questions.models import Question


# VIEWS
def index(request):
    # Get all the questions
    question_list = Question.objects.order_by("-pub_date")

    # Render the template
    return render(request, "questions/index.html", {"question_list": question_list})


def display_question(request, question_id):
    # Try to get the question that has the given question id
    question = get_object_or_404(Question, pk=question_id)

    # Render the template
    return render(request, "questions/question.html", {"question": question})
