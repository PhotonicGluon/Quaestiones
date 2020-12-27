"""
models.py

Created on 2020-12-26
Updated on 2020-12-26

Copyright © Ryan Kan

Description: The models for the `questions` application.
"""

# IMPORTS
from django.db import models


# MODELS
class Question(models.Model):
    # Attributes
    title = models.CharField("Title", max_length=100)
    short_description = models.CharField("Summary of Question", max_length=200)
    long_description = models.TextField("Description", max_length=10000)
    pub_date = models.DateTimeField("Date Published", auto_now=True)

    # Methods
    def __str__(self):
        return self.title
