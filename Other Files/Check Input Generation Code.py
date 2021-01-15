"""
Check Input Generation Code.py

Created on 2020-12-30
Updated on 2021-01-15

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
globalsDict = {}
exec(INPUT_GENERATION_FUNCTION, globalsDict)

# CHECKS
# Check to see if the function actually exists
try:
    outputs = globalsDict["input_generation"]()
except NameError:
    raise NameError("Your input generation code does not contain a function "
                    "called `input_generation`.")

# Check to see if it returns exactly two things
assert len(outputs) == 2, "The `input_generation` function DOES NOT return " \
                          f"TWO things. (It returned {len(outputs)} things)."

# Split the outputs into the input and the answer
input_, answer = outputs

# Check if the function returns the correct types of things
if not isinstance(input_, str):
    raise ValueError("The input that is returned by the `input_generation` "
                     "function is NOT a string. Returned a/an "
                     f"`{str(type(input_))[8:-2]}`:\n{input_}")

if not isinstance(answer, str):
    raise ValueError("The answer that is returned by the `input_generation` "
                     "function is NOT a string. Returned a/an "
                     f"`{str(type(answer))[8:-2]}`:\n{answer}")

# OUTPUT
# Report that everything went well
print("Your input generation code is VALID.")
