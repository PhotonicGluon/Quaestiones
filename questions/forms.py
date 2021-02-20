"""
forms.py

Created on 2021-01-17
Updated on 2021-02-20

Copyright © Ryan Kan

Description: The forms for the `questions` application.
"""

# IMPORTS
import math

from django import forms

from Quaestiones.settings import CUTOFF_SOLVER
from questions.models import Question


# CLASSES
class EditQuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ["title", "points", "short_description", "long_description", "input_generation_code",
                  "question_release_datetime"]
        widgets = {
            "question_release_datetime": forms.DateTimeInput(attrs={"placeholder": "YYYY-MM-DD HH:MM:SS"})
        }

    # Methods
    def clean_points(self):
        """
        This method will be called when the points value needs to be cleaned.

        Returns:
            int:
                The processed points value.

        Raises:
            forms.ValidationError:
                If the value of points is less than the value of `math.floor(math.log2(CUTOFF_SOLVER + 1))`
        """

        min_points = math.floor(math.log2(CUTOFF_SOLVER + 1))
        if self.cleaned_data["points"] < min_points:
            raise forms.ValidationError(f"The points value for the question must be at least {min_points}.")
        else:
            return self.cleaned_data["points"]

    def clean_input_generation_code(self):
        """
        This method will be called when the input generation code needs to be cleaned.

        Returns:
            str:
                The processed input generation code.

        Raises:
            forms.ValidationError:
                If the input generation code is invalid.
        """

        # Run the input generation code and catch any errors thrown
        temp = {}

        try:
            exec(self.cleaned_data["input_generation_code"], temp)
        except Exception as e:
            error_type = e.__repr__().split("(")[0]
            error_msg = e.__str__()

            raise forms.ValidationError(f"Caught a '{error_type}' in your input generation code: {error_msg}")

        # Check to see if the function actually exists
        try:
            outputs = temp["input_generation"]()
        except KeyError:
            raise forms.ValidationError("Your input generation code does not contain a function called "
                                        "`input_generation`.")
        except Exception as e:
            error_type = e.__repr__().split("(")[0]
            error_msg = e.__str__()

            raise forms.ValidationError(f"Caught a '{error_type}' in your input generation code: {error_msg}")

        # Check to see if it returns exactly two things
        if not isinstance(outputs, tuple) or len(outputs) != 2:
            raise forms.ValidationError("The `input_generation` function DOES NOT return TWO things.")

        # Split the outputs into the input and the answer
        input_, answer = outputs

        # Check if the function returns the correct types of things
        if not isinstance(input_, str):
            raise forms.ValidationError(f"The input that is returned by the `input_generation` function is NOT a "
                                        f"string. It returned a/an `{str(type(input_))[8:-2]}`.")

        if not isinstance(answer, str):
            raise forms.ValidationError(f"The answer that is returned by the `input_generation` function is NOT a "
                                        f"string. It returned a/an `{str(type(answer))[8:-2]}`.")

        # Return the string of the input generation code
        return self.cleaned_data["input_generation_code"]
