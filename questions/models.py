"""
models.py

Created on 2020-12-26
Updated on 2020-12-30

Copyright © Ryan Kan

Description: The models for the `questions` application.
"""

# IMPORTS
from django.db import models
from markdown import markdown


# MODELS
class Question(models.Model):
    # Attributes
    title = models.CharField("Title", max_length=100)
    short_description = models.CharField("Summary of Question", max_length=200)
    long_description = models.TextField("Description", max_length=10000)
    pub_date = models.DateTimeField("Date Published", auto_created=True)
    last_updated = models.DateTimeField("Last Updated", auto_now=True)

    # Methods
    def html_of_description(self):
        # Convert the markdown code in the `self.long_description` to HTML
        html = markdown(self.long_description, extensions=["fenced_code"])

        # Return the final HTML text
        return html

    def __str__(self):
        return self.title
