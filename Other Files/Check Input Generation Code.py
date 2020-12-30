"""
Check Input Generation Code.py

Created on 2020-12-30
Updated on 2020-12-30

Copyright © Ryan Kan

Description: Checks whether the input generation code that you have written
             meets the requirements in the `README.md` file.
"""

# CONSTANTS
# Paste your input generation code in the string below
# Note: Escape all backslashes with "\\". (e.g. "\n" --> "\\n"; "\t" --> "\\t";
#       "\\" --> "\\\\")
INPUT_GENERATION_FUNCTION = """REPLACE THIS LINE WITH YOUR FUNCTION"""

# Run the input generation code
exec(INPUT_GENERATION_FUNCTION)

# CHECKS
# Check to see if the function actually exists
try:
    input_generation()
except NameError:
    raise NameError("Your input generation code does not contain a function "
                    "called `input_generation`.")

# Check to see if it returns exactly two things
try:
    input_, answer = input_generation()
except ValueError as e:
    raise AssertionError("The `input_generation` function DOES NOT return TWO "
                         "things.")

# Check if the function returns the correct types of things
if not isinstance(input_, str):
    raise ValueError("The input that is returned by the `input_generation` "
                     "function is NOT a string. Returned a "
                     f"{type(input_)}:\n{input_}")

if not isinstance(answer, str):
    raise ValueError("The answer that is returned by the `input_generation` "
                     "function is NOT a string. Returned a "
                     f"{type(answer)}:\n{answer}")

# OUTPUT
# Report that everything went well
print("Your input generation code is VALID.")
