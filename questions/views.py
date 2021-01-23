"""
views.py

Created on 2020-12-26
Updated on 2021-01-23

Copyright © Ryan Kan

Description: The views for the `questions` app.
"""

# IMPORTS
import logging
import os

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from ratelimit import ALL as RATELIMIT_ALL
from ratelimit.decorators import ratelimit

from Quaestiones.settings.common import MEDIA_ROOT
from questions.forms import EditQuestionForm
from questions.models import Question

# SETUP
logger = logging.getLogger("Quaestiones")


# VIEWS
# Main Views
@ratelimit(key="ip", rate="3/s", method=RATELIMIT_ALL)
def index(request):
    # Check if the request was ratelimited
    was_limited = getattr(request, "limited", False)

    if was_limited:
        return plea_for_no_automated_requests(request)

    # Get all the questions
    question_list = Question.objects.order_by("pub_date")

    # Render the template
    return render(request, "questions/index.html", {"question_list": question_list})


@ratelimit(key="ip", rate="3/s", method=RATELIMIT_ALL)
def display_question(request, question_id):
    # Check if the request was ratelimited
    was_limited = getattr(request, "limited", False)

    if was_limited:
        return plea_for_no_automated_requests(request)

    # Try to get the question that has the given question id
    question = get_object_or_404(Question, pk=question_id)

    # Check if the question can be accessed
    if question.is_question_released():
        # Get the current user's solved puzzles list
        user = request.user

        if user.is_authenticated:
            solved_puzzles = user.profile.solved_questions

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

    logger.info(f"Someone tried to access the question with id '{question_id}' before the question was released.")
    return HttpResponse("The question will be released on the time specified. Please do not send automatic requests to "
                        "this page! :)", content_type="text/plain", status=403)


@ratelimit(key="ip", rate="3/s", method=RATELIMIT_ALL)
def generate_input(request, question_id):
    # Check if the request was ratelimited
    was_limited = getattr(request, "limited", False)

    if was_limited:
        return plea_for_no_automated_requests(request)

    if request.method == "GET":
        # Try to get the question that has the given question id
        question = get_object_or_404(Question, pk=question_id)

        if question.is_question_released():
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
                return HttpResponse("The puzzles' inputs differ by user. Please log in or sign up to get your own "
                                    "unique puzzle input and to participate.", content_type="text/plain")

        logger.info(f"Someone tried to access the question with id '{question_id}' before the question was released.")
        return HttpResponse("The question will be released on the time specified. Please do not send automatic "
                            "requests to this page! :)", content_type="text/plain", status=403)

    return HttpResponse("The POST request is not supported on this page.", content_type="text/plain")


@ratelimit(key="ip", rate="3/s", method=RATELIMIT_ALL)
def check_question_answer(request, question_id):
    # Check if the request was ratelimited
    was_limited = getattr(request, "limited", False)

    if was_limited:
        return plea_for_no_automated_requests(request)

    if request.method == "POST":
        # Get the user that has just requested to check the answer
        user = request.user
        username = user.username

        # Get the user's answer
        user_answer = request.POST["answer"]

        # Get the correct answer for the user's input
        input_generated = True
        try:
            with open(os.path.join(MEDIA_ROOT, f"{username}/{question_id}.out"), "r") as f:
                correct_answer = f.read()
                f.close()
        except FileNotFoundError:
            correct_answer = None
            input_generated = False  # The user hasn't generated the input yet!

        # Check if the user can check the answer
        can_check_answer, time_left = user.profile.check_timeout_question(question_id)
        if can_check_answer:
            # Check if the two answers are equal
            if user_answer == correct_answer:  # User answered the question correctly
                # Check if the user is just resubmitting the form
                if str(question_id) in user.profile.get_solved_questions():
                    return redirect("index")

                # If not, the user just answered the question correctly
                logger.info(f"'{username}' answered the question with id '{question_id}' correctly.")

                # Add the question to the user's list of correct questions
                user.profile.add_solved_question(question_id)

                # Render the answer page
                return render(request, "questions/answer.html", {"correct": True})

        # If the code reaches here, then the user was incorrect OR is not allowed to submit the form again
        # Get the `incorrect_type`
        context = {}
        if not input_generated:
            incorrect_type = "input not generated"

        elif not can_check_answer:
            incorrect_type = "cannot check yet"
            context = {"correct": False, "incorrect_type": incorrect_type, "question_id": question_id,
                       "time_left": time_left}

        elif user_answer == "":  # Nothing was typed
            incorrect_type = "nothing entered"

        elif not user_answer.isdigit() and correct_answer.isdigit():
            incorrect_type = "not a number"

        elif user_answer < correct_answer:
            incorrect_type = "too low"

        else:
            incorrect_type = "too high"

        # Determine whether or not to timeout the user
        if incorrect_type in ["too low", "too high"]:
            user.profile.add_timeout_question(question_id)

        # Form the context dictionary
        if context == {}:
            context = {"correct": False, "incorrect_type": incorrect_type, "question_id": question_id}

        # Render the answer page
        logger.info(
            f"'{username}' answered the question with id '{question_id}' incorrectly. (Reason: {incorrect_type})")

        return render(request, "questions/answer.html", context)

    return redirect("display_question", question_id=question_id)


# Admin-accessible Views
@ratelimit(key="ip", rate="3/s", method=RATELIMIT_ALL)
@staff_member_required(login_url="/login/")
def reset_question_input(request, question_id):
    # Check if the request was ratelimited
    was_limited = getattr(request, "limited", False)

    if was_limited:
        return plea_for_no_automated_requests(request)

    # Check if the request was a post request
    if request.method == "POST":
        # Get the user that has just requested to reset the input
        user = request.user

        # Check if the user has superuser status
        if user.is_superuser:
            # Get all folders in the media folder
            users_folders = [x for x in os.listdir(MEDIA_ROOT) if os.path.isdir(os.path.join(MEDIA_ROOT, x))]

            # Go through every user's folder and delete the corresponding input
            for username in users_folders:
                # Delete the input and output of the question with the question id
                try:
                    os.remove(os.path.join(MEDIA_ROOT, f"{username}/{question_id}.in"))
                    os.remove(os.path.join(MEDIA_ROOT, f"{username}/{question_id}.out"))
                except FileNotFoundError:
                    pass

                # Get the user associated with the username
                user_ = User.objects.get(username=username)

                # Remove the question id from the user's solved puzzles
                user_.profile.remove_solved_question(question_id)

            logger.info(
                f"The superuser '{user.username}' reset the question input for the question with id '{question_id}'.")
            return HttpResponse("Operation Complete", content_type="text/plain")
        else:
            return HttpResponse("Forbidden", status=403, content_type="text/plain")
    else:
        return HttpResponse("Invalid Method", status=404, content_type="text/plain")


@ratelimit(key="ip", rate="3/s", method=RATELIMIT_ALL)
@staff_member_required(login_url="/login/")
def edit_questions_view(request):
    # Check if the request was ratelimited
    was_limited = getattr(request, "limited", False)

    if was_limited:
        return plea_for_no_automated_requests(request)

    # Get all the questions
    question_list = Question.objects.order_by("pub_date")

    # Render the template
    return render(request, "questions/edit_questions.html", {"question_list": question_list})


@ratelimit(key="ip", rate="3/s", method=RATELIMIT_ALL)
@staff_member_required(login_url="/login/")
def edit_question_view(request, question_id=None):
    # Check if the request was ratelimited
    was_limited = getattr(request, "limited", False)

    if was_limited:
        return plea_for_no_automated_requests(request)

    if request.method == "POST":
        # Create the form object
        if Question.objects.filter(pk=question_id).exists():  # The question already exists
            # Then update the question by filling in the form
            question = Question.objects.get(pk=question_id)
            form = EditQuestionForm(request.POST, instance=question)  # Pass the data from the POST request

            # Get the reset input url
            reset_input_url = "http://" + get_current_site(request).domain + question.question_input_reset_link()

            # Form the regex for the deletion command
            regex_for_deletion = "".join([f"[{char.lower()}{char.upper()}]" for char in question.title])

        else:
            # This is a new question; just fill in the form using the POST data
            form = EditQuestionForm(request.POST)
            reset_input_url = ""
            regex_for_deletion = ""

        # Check if the form is valid
        if form.is_valid():
            # Save the edited question to the database
            form.save()

            # Redirect back to the edit questions view
            return redirect("edit_questions")

    else:
        # See if the question already exists
        if Question.objects.filter(pk=question_id).exists():
            # Fill in the `EditQuestionForm` with the information of the question
            question = Question.objects.get(pk=question_id)
            form = EditQuestionForm(instance=question)

            # Get the reset input url
            reset_input_url = "http://" + get_current_site(request).domain + question.question_input_reset_link()

            # Form the regex for the deletion command
            regex_for_deletion = "".join([f"[{char.lower()}{char.upper()}]" for char in question.title])

        else:
            # The user wants to create a new question
            form = EditQuestionForm()
            reset_input_url = ""
            regex_for_deletion = ""

    return render(request, "questions/edit_question.html", {"form": form, "reset_input_url": reset_input_url,
                                                            "regex_for_deletion": regex_for_deletion})


@ratelimit(key="ip", rate="3/s", method=RATELIMIT_ALL)
@staff_member_required(login_url="/login/")
def preview_question_view(request):
    return render(request, "questions/preview_question.html")


@ratelimit(key="ip", rate="3/s", method=RATELIMIT_ALL)
@staff_member_required(login_url="/login/")
def delete_question_view(request, question_id):
    if request.method == "POST":  # This is coming from the edit question page
        # Get the question to be deleted
        question = get_object_or_404(Question, id=question_id)

        # Report the deletion to the logs
        logger.info(f"'{request.user.username}' has just deleted the question with id '{question.id}'.")

        # Perform the deletion
        question.delete()

        # Remove that question's input from all users
        reset_question_input(request, question_id)

    # Show the edit questions page
    return redirect("edit_questions")


# Other Views
def plea_for_no_automated_requests(request):
    logger.warning(f"Someone from the IP address {request.META['REMOTE_ADDR']} is sending too many requests!")
    return HttpResponse("Please do not send requests this fast to the website! You'll make me sad if you do :(",
                        content_type="text/plain")
