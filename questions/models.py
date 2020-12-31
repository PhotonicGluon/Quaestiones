"""
models.py

Created on 2020-12-26
Updated on 2020-12-31

Copyright © Ryan Kan

Description: The models for the `questions` application.
"""

# IMPORTS
from django.db import models
from markdown import markdown


# MODELS
class Question(models.Model):
    # Modifiable Attributes
    title = models.CharField("Title", max_length=100)
    short_description = models.CharField("Summary of Question", max_length=200, blank=True, null=True,
                                         help_text="A short summary should suffice.")
    long_description = models.TextField("Description", max_length=10000,
                                        help_text="Write this in the Markdown language!")

    input_generation_code = models.TextField("Input Generation Code",
                                             help_text="Make sure to follow the specifications in the README.md file!")

    # Non-modifiable Attributes
    pub_date = models.DateTimeField("Date Published", auto_now_add=True)
    last_updated = models.DateTimeField("Last Updated", auto_now=True)

    # Methods
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

    def __str__(self):
        return self.title
