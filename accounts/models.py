"""
models.py

Created on 2020-12-31
Updated on 2021-01-01

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

    # Stores the ids of the solved puzzles
    solved_puzzles = models.TextField(default="", blank=True, null=True)

    # Stores the ids of questions where the user has to wait before answering again
    timeout_puzzles = models.TextField(default="", blank=True, null=True)

    # Methods
    # Solved Puzzles
    def get_solved_puzzles(self):
        """
        Gets the list of puzzles solved by the user.

        Returns:
            list[str]:
                IDs of the puzzles solved.
        """

        # Get the raw list of solved puzzles
        solved_puzzles = self.solved_puzzles.split(",")

        # Remove the empty string element from `solved_puzzles`, if it is in there
        if "" in solved_puzzles:
            solved_puzzles.remove("")

        # Return `solved_puzzles`
        return solved_puzzles

    def add_solved_puzzle(self, question_id):
        """
        Add the `question_id` into the list of solved puzzles by the user.

        Args:
            question_id (union[str, int])
        """

        solved_puzzles = self.get_solved_puzzles()
        solved_puzzles.append(str(question_id))
        self.solved_puzzles = ",".join(solved_puzzles)
        self.save()

    def remove_solved_puzzle(self, question_id):
        """
        Removes the `question_id` into the list of solved puzzles by the user.

        Args:
            question_id (union[str, int])
        """

        solved_puzzles = self.get_solved_puzzles()

        try:
            solved_puzzles.remove(str(question_id))
        except ValueError:
            pass

        self.solved_puzzles = ",".join(solved_puzzles)
        self.save()

    def puzzles_solved(self):
        """
        Get the number of puzzles solved by the user.

        Returns:
            int
        """

        return len(self.get_solved_puzzles())

    def solved_all_puzzles(self):
        """
        Returns whether the user had solved all the available puzzles.

        Returns:
            bool
        """

        return len(self.get_solved_puzzles()) == Question.objects.count()

    # Timeout Puzzles
    def get_timeout_puzzles(self):
        """
        Gets the dictionary of puzzles which the user needs to wait before answering again.

        Returns:
            dict[str, int]:
                A dictionary mapping from the puzzle ID to the next time when the user can answer the question again.
        """

        # Get the raw list of timeout puzzles
        timeout_puzzles = self.timeout_puzzles.split(",")

        # Remove the empty string element from `timeout_puzzles`, if it is in there
        if "" in timeout_puzzles:
            timeout_puzzles.remove("")

        # Turn the raw list into a dictionary
        dictionary = defaultdict(int)
        for timeout_puzzle in timeout_puzzles:
            entry, value = timeout_puzzle.split(":")
            dictionary[entry] = int(value)

        # Return the timeout puzzles dictionary
        return dictionary

    def add_timeout_puzzle(self, question_id, timeout_amount=60):
        """
        Adds a question to the timeout list.

        Args:
            question_id (int)
            timeout_amount (int):
                The time, in seconds, to make the user wait before allowing them to answer the question again.
                (Default = 60)
        """

        # Get the dictionary of timeout puzzles
        timeout_puzzles = self.get_timeout_puzzles()

        # Get the current UNIX epoch time
        time_value = int(time()) + 1  # Consider the next second

        # Increment the `time_value` by the `timeout_amount`
        time_value += timeout_amount

        # Set the question's the timeout value
        timeout_puzzles[str(question_id)] = time_value

        # Save the timeout puzzles list
        self.save_timeout_puzzles(timeout_puzzles)

    def check_timeout_puzzle(self, question_id):
        """
        Checks whether a puzzle can be submitted again.

        Args:
            question_id (int)

        Returns:
            bool:
                Whether the user can check their answer.
            int:
                How long more before the user can check their answer.
        """

        # Get the dictionary of timeout puzzles
        timeout_puzzles = self.get_timeout_puzzles()

        # Get the current UNIX epoch time
        time_value = int(time()) + 1  # Consider the next second

        # Compare the question's the timeout value with the current time
        if timeout_puzzles[str(question_id)] <= time_value:
            # Then it can be accessed
            return True, -1

        return False, timeout_puzzles[str(question_id)] - time_value

    def save_timeout_puzzles(self, timeout_puzzles):
        """
        Saves the timeout puzzles dictionary as a string.

        Args:
            timeout_puzzles (dict[str, int])
        """

        # Convert the `timeout_puzzles` dictionary into a string
        strings = []
        for key, value in timeout_puzzles.items():
            strings.append(f"{key}:{value}")

        string = ",".join(strings)

        # Update the user's profile
        self.timeout_puzzles = string
        self.save()


# FUNCTIONS
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    # 'Delete' unused variables
    _ = sender
    _ = kwargs

    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    # 'Delete' unused variables
    _ = sender
    _ = kwargs

    instance.profile.save()
