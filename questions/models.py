"""
models.py

Created on 2020-12-26
Updated on 2021-01-02

Copyright © Ryan Kan

Description: The models for the `questions` application.
"""

# IMPORTS
from datetime import datetime

from django.db import models
from django.urls import reverse, exceptions
from markdown import markdown


# MODELS
class Question(models.Model):
    # Todo: add support for 'invisible' questions that are not visible to anyone and do not count towards the question
    #       tally
    # Modifiable Attributes
    title = models.CharField("Title", max_length=50)
    short_description = models.CharField("Summary of Question", max_length=200, blank=True, null=True,
                                         help_text="A short summary should suffice.")
    long_description = models.TextField("Description", max_length=10000,
                                        help_text="Write this in the Markdown language!")
    question_release_datetime = models.DateTimeField("Question Release Date-Time", editable=True,
                                                     help_text="When should this question be released?")
    input_generation_code = models.TextField("Input Generation Code",
                                             help_text="Make sure to follow the specifications in the README.md file!")
    override_key = models.CharField("Override Key", max_length=10,
                                    help_text="If the question is inaccessible, enter the full url to the question, "
                                              "followed by 'OK=', followed by this key to access it.")

    # Non-modifiable Attributes
    pub_date = models.DateTimeField("Date Published", auto_now_add=True)
    last_updated = models.DateTimeField("Last Updated", auto_now=True)

    # Methods
    def question_input_reset_link(self):
        """
        Returns the link for an admin to reset the input for this question for all users.

        Returns:
            str
        """

        try:
            link = reverse("reset_question_input", kwargs={"question_id": self.id})
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

    def __str__(self):
        return self.title
