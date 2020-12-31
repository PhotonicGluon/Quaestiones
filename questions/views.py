"""
views.py

Created on 2020-12-26
Updated on 2020-12-31

Copyright © Ryan Kan

Description: The views for the `questions` app.
"""

# IMPORTS
import logging
import os

from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404

from Quaestiones.settings.common import MEDIA_ROOT
from questions.models import Question

# SETUP
logger = logging.getLogger("Quaestiones")


# VIEWS
def index(request):
    # Get all the questions
    question_list = Question.objects.order_by("pub_date")

    # Render the template
    return render(request, "questions/index.html", {"question_list": question_list})


def display_question(request, question_id):
    # Try to get the question that has the given question id
    question = get_object_or_404(Question, pk=question_id)

    # Get the current user's solved puzzles list
    user = request.user

    if user.is_authenticated:
        solved_puzzles = user.profile.solved_puzzles

        # Generate the context based on whether the user has already solved this question
        if str(question_id) in solved_puzzles.split(","):  # Solved already
            # Get the user's answer
            with open(os.path.join(MEDIA_ROOT, f"{user.username}/{question_id}.out"), "r") as f:
                answer = f.read()
                f.close()

            # Craft the context
            context = {"question": question, "already_answered_correctly": True, "correct_answer": answer}

        else:
            context = {"question": question}
    else:
        context = {"question": question}

    # Render the template
    return render(request, "questions/question.html", context)


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
                logger.info(f"Generating input for '{username}' for the question with id '{question_id}'.")
                input_, answer = temp_dictionary["input_generation"]()

                # Save them to files
                try:
                    os.mkdir(os.path.join(MEDIA_ROOT, username))
                except OSError:
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
            return HttpResponse("The puzzles' inputs differ by user. Please log in or sign up to get your own unique "
                                "puzzle input and to participate.", content_type="text/plain")
    else:
        return HttpResponse("The GET request is not supported on this page.", content_type="text/plain")


def check_question_answer(request, question_id):
    if request.method == "POST":
        # Get the username of the user that has just requested to check the answer
        user = request.user
        username = user.username

        # Get the user's answer
        user_answer = request.POST["answer"]

        # Get the correct answer for the user's input
        with open(os.path.join(MEDIA_ROOT, f"{username}/{question_id}.out"), "r") as f:
            correct_answer = f.read()
            f.close()

        # Check if the two answers are equal
        if user_answer == correct_answer:  # User answered the question correctly
            logger.info(f"'{username}' answered the question with id '{question_id}' correctly.")

            # Add the question to the user's list of correct questions
            user.profile.add_solved_puzzle(question_id)

            # Render the answer page
            return render(request, "questions/answer.html", {"correct": True})

        else:  # User answered the question incorrectly
            # Get the `incorrect_type`
            if user_answer == "":  # Nothing was typed
                incorrect_type = "nothing entered"
            elif not user_answer.isdigit() and correct_answer.isdigit():
                incorrect_type = "not a number"
            elif user_answer < correct_answer:
                incorrect_type = "too low"
            else:
                incorrect_type = "too high"

            # Render the answer page
            logger.info(
                f"'{username}' answered the question with id '{question_id}' incorrectly. (Reason: {incorrect_type})")

            return render(request, "questions/answer.html",
                          {"correct": False, "incorrect_type": incorrect_type, "question_id": question_id})

    return redirect("display_question", question_id=question_id)
