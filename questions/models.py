"""
models.py

Created on 2020-12-26
Updated on 2021-01-26

Copyright © Ryan Kan

Description: The models for the `questions` application.
"""

# IMPORTS
import sys
from datetime import datetime
from random import shuffle, seed

from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse, exceptions
from markdown import markdown


# MODELS
class Question(models.Model):
    # Modifiable Attributes
    title = models.CharField("Title", max_length=50)
    short_description = models.CharField("Summary of Question", max_length=200, blank=True, null=True)
    long_description = models.TextField("Description", max_length=10000,
                                        help_text="Write this in the Markdown language.")
    question_release_datetime = models.DateTimeField("Question Release Datetime", editable=True,
                                                     help_text="When should this question be released?")
    input_generation_code = models.TextField("Input Generation Code",
                                             help_text="Make sure to follow the specifications in the README.md file.")
    question_slug = models.SlugField(help_text="This was automatically generated when the question is created.")

    # Read-only Attributes
    pub_date = models.DateTimeField("Date Published", auto_now_add=True)
    last_updated = models.DateTimeField("Last Updated", auto_now=True)
    num_solves = models.IntegerField("Number of users that solved this question", default=0, blank=True, null=True)

    # Default Methods
    def save(self, *args, **kwargs):
        """
        Save the current instance.
        """

        # If the question has not been created yet, update the question's slug
        if not self.id:
            self.question_slug = slugify(self.title)

        super(Question, self).save(*args, **kwargs)

    # Custom Methods
    def question_input_reset_link(self):
        """
        Returns the link for an admin to reset the input for this question for all users.

        Returns:
            str
        """

        try:
            link = reverse("reset_question_input", kwargs={"question_slug": self.question_slug})
        except exceptions.NoReverseMatch:
            link = "This will be generated once the question is created."

        return link

    def html_of_description(self):
        """
        Returns the HTML version of the markdown text in `self.long_description`.

        Returns:
            str:
                The HTML code.
        """

        # Convert the markdown code to HTML
        html = markdown(self.long_description, extensions=["fenced_code", "sane_lists"])

        # Return the final HTML text
        return html

    def is_question_released(self):
        """
        Whether or not the question was already released.

        Returns:
            bool
        """

        return datetime.timestamp(self.question_release_datetime) <= datetime.timestamp(datetime.now())

    def get_seed_value(self):
        """
        Gets the random seed value for any randomizers of this question.

        Returns:
            int:
                The seed value.
        """

        return int.from_bytes(bytes(self.title, "UTF-8"), sys.byteorder) + int(
            self.question_release_datetime.timestamp())

    def scrambled_title(self):
        """
        Makes the question's title scrambled so that the users cannot cheat and see the actual name of the puzzle.

        Returns:
            str:
                The scrambled title.
        """

        seed(self.get_seed_value())  # Makes it so that the scrambled title will always be the same
        title = list(self.title)
        shuffle(title)
        return "".join(title)

    def __str__(self):
        return self.title
