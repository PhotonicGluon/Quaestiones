"""
views.py

Created on 2020-12-26
Updated on 2020-12-26

Copyright © Ryan Kan

Description: The views for the `questions` app.
"""

# IMPORTS
import os

from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404

from Quaestiones.settings.common import MEDIA_ROOT
from questions.models import Question


# VIEWS
def index(request):
    # Get all the questions
    question_list = Question.objects.order_by("pub_date")

    # Render the template
    return render(request, "questions/index.html", {"question_list": question_list})


def display_question(request, question_id):
    # Try to get the question that has the given question id
    question = get_object_or_404(Question, pk=question_id)

    # Render the template
    return render(request, "questions/question.html", {"question": question})


def generate_input(request, question_id):
    if request.method == "GET":
        if request.user.is_authenticated:
            # Get the username of the user that has just requested to generate the input
            username = request.user.username

            # Check if the input file already exists
            if os.path.isfile(os.path.join(MEDIA_ROOT, f"{username}/{question_id}.in")):
                # Then read the file
                with open(os.path.join(MEDIA_ROOT, f"{username}/{question_id}.in"), "r") as f:
                    input_ = f.read()
                    f.close()
            else:
                # Try to get the question that has the given question id
                question = get_object_or_404(Question, pk=question_id)

                # Get the input generation code from there
                input_generation_code = question.input_generation_code

                # Execute it
                temp_dictionary = {}
                exec(input_generation_code, temp_dictionary)

                # Get the input and answer for the user
                input_, answer = temp_dictionary["input_generation"]()

                # Save them to files
                try:
                    os.mkdir(os.path.join(MEDIA_ROOT, username))
                except OSError as e:
                    print(e)
                    pass

                with open(os.path.join(MEDIA_ROOT, f"{username}/{question_id}.in"), "w+") as f:
                    f.write(input_)
                    f.close()

                with open(os.path.join(MEDIA_ROOT, f"{username}/{question_id}.out"), "w+") as f:
                    f.write(answer)
                    f.close()

            return HttpResponse(input_, content_type="text/plain")
        else:
            # This user has not logged in
            return HttpResponse("Puzzle inputs differ by user. Please log in or sign up to get your own unique puzzle "
                                "input.", content_type="text/plain")
    else:
        return HttpResponse("The GET request is not supported on this page.", content_type="text/plain")


def check_question_answer(request, question_id):
    if request.method == "POST":
        # Get the username of the user that has just requested to check the answer
        username = request.user.username

        # Get the user's answer
        user_answer = request.POST["answer"]

        # Get the correct answer for the user's input
        with open(os.path.join(MEDIA_ROOT, f"{username}/{question_id}.out"), "r") as f:
            correct_answer = f.read()
            f.close()

        # Check if they are the same
        if user_answer == correct_answer:
            # TODO: Do something
            return HttpResponse("Correct", content_type="text/plain")
        else:
            # TODO: Do something else
            return HttpResponse("Incorrect", content_type="text/plain")

    return redirect("index")
