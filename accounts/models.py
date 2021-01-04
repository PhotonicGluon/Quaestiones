"""
models.py

Created on 2020-12-31
Updated on 2021-01-04

Copyright © Ryan Kan

Description: The models for the `accounts` application.
"""

# IMPORTS
from collections import defaultdict
from time import time

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from questions.models import Question


# MODELS
class Profile(models.Model):
    # Attributes
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Get the user that the profile is 'attached' to

    # Editable Fields
    bio = models.TextField(default="", blank=True, null=True)

    # Admin-editable Fields
    solved_questions = models.TextField(default="", blank=True, null=True)
    timeout_questions = models.TextField(default="", blank=True, null=True)

    # Methods
    def get_solved_questions(self):
        """
        Gets the list of questions solved by the user.

        Returns:
            list[str]:
                IDs of the questions solved.
        """

        # Get the raw list of the solved questions' IDs
        solved_questions = self.solved_questions.split(",")

        # Remove the empty string element from `solved_questions`, if it is in there
        if "" in solved_questions:
            solved_questions.remove("")

        # Return `solved_questions`
        return solved_questions

    def add_solved_question(self, question_id):
        """
        Add the `question_id` into the list of solved questions by the user.

        Args:
            question_id (union[str, int])
        """

        solved_questions = self.get_solved_questions()
        solved_questions.append(str(question_id))

        self.solved_questions = ",".join(solved_questions)
        self.save()

    def remove_solved_question(self, question_id):
        """
        Removes the `question_id` into the list of solved questions by the user.

        Args:
            question_id (union[str, int])
        """

        solved_questions = self.get_solved_questions()

        try:
            solved_questions.remove(str(question_id))
        except ValueError:
            pass

        self.solved_questions = ",".join(solved_questions)
        self.save()

    def no_questions_solved(self):
        """
        Get the number of questions solved by the user.

        Returns:
            int
        """

        return len(self.get_solved_questions())

    def has_solved_all_questions(self):
        """
        Returns whether the user had solved all the available questions.

        Returns:
            bool
        """

        return self.no_questions_solved() == Question.objects.count()

    def get_timeout_questions(self):
        """
        Gets the dictionary of questions which the user needs to wait before answering again.

        Returns:
            dict[str, int]:
                A dictionary mapping from the question ID to the next time when the user can answer the question again.
        """

        # Get the raw list of timeout questions
        timeout_questions = self.timeout_questions.split(",")

        # Remove the empty string element from `timeout_questions`, if it is in there
        if "" in timeout_questions:
            timeout_questions.remove("")

        # Turn the raw list into a dictionary
        dictionary = defaultdict(int)
        for timeout_puzzle in timeout_questions:
            entry, value = timeout_puzzle.split(":")
            dictionary[entry] = int(value)

        # Return the timeout questions dictionary
        return dictionary

    def add_timeout_question(self, question_id, timeout_amount=60):
        """
        Adds a question to the timeout list.

        Args:
            question_id (int)
            timeout_amount (int):
                The time, in seconds, to make the user wait before allowing them to answer the question again.
                (Default = 60)
        """

        # Get the dictionary of timeout questions
        timeout_questions = self.get_timeout_questions()

        # Get the current UNIX epoch time
        time_value = int(time()) + 1  # Consider the next second

        # Increment the `time_value` by the `timeout_amount`
        time_value += timeout_amount

        # Set the question's the timeout value
        timeout_questions[str(question_id)] = time_value

        # Save the timeout questions dictionary
        self.save_timeout_question(timeout_questions)

    def check_timeout_question(self, question_id):
        """
        Checks whether a question can be submitted again.

        Args:
            question_id (int)

        Returns:
            bool:
                Whether the user can check their answer.
            int:
                How long more before the user can check their answer. If it is `-1` then it can be checked immediately.
        """

        # Get the dictionary of timeout puzzles
        timeout_puzzles = self.get_timeout_questions()

        # Get the current UNIX epoch time
        time_value = int(time()) + 1  # Consider the next second

        # Compare the question's the timeout value with the current time
        if timeout_puzzles[str(question_id)] <= time_value:
            # Then it can be accessed
            return True, -1

        # If not, then return how long more the user has to wait
        return False, timeout_puzzles[str(question_id)] - time_value

    def save_timeout_question(self, timeout_questions):
        """
        Saves the timeout questions dictionary as a string.

        Args:
            timeout_questions (dict[str, int])
        """

        # Convert the `timeout_questions` dictionary into a string
        strings = []
        for key, value in timeout_questions.items():
            strings.append(f"{key}:{value}")

        string = ",".join(strings)

        # Update the user's profile
        self.timeout_questions = string
        self.save()


# FUNCTIONS
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    # Delete unused variables
    _ = sender
    _ = kwargs

    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    # Delete unused variables
    _ = sender
    _ = kwargs

    instance.profile.save()
