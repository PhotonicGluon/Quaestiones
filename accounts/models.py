"""
models.py

Created on 2020-12-31
Updated on 2021-01-01

Copyright © Ryan Kan

Description: The models for the `accounts` application.
"""

# IMPORTS
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from questions.models import Question


# MODELS
class Profile(models.Model):
    # Attributes
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Get the user that the profile is 'attached' to

    solved_puzzles = models.TextField(default="", blank=True, null=True)  # Stores the ids of the solved puzzles

    # Methods
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
