"""
forms.py

Created on 2021-01-17
Updated on 2021-01-18

Copyright © Ryan Kan

Description: The forms for the `questions` application.
"""

# IMPORTS
from django import forms

from questions.models import Question


# CLASSES
class EditQuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ["title", "short_description", "long_description", "input_generation_code",
                  "question_release_datetime", "override_key"]
        widgets = {
            "title": forms.TextInput(),
            "short_description": forms.TextInput(),
            "long_description": forms.Textarea(),
            "input_generation_code": forms.Textarea(),
            "question_release_datetime": forms.DateTimeInput(),
            "override_key": forms.TextInput(),
        }

    # Methods
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

        # Run the input generation code
        temp = {}
        exec(self.cleaned_data["input_generation_code"], temp)

        # Check to see if the function actually exists
        try:
            outputs = temp["input_generation"]()
        except KeyError:
            raise forms.ValidationError("Your input generation code does not contain a function called "
                                        "`input_generation`.")
        except Exception as e:
            raise forms.ValidationError(f"There was an error in your code: {e}")

        # Check to see if it returns exactly two things
        if not isinstance(outputs, tuple) and len(outputs) != 2:
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
