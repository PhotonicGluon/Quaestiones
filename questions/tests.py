"""
tests.py

Created on 2020-12-26
Updated on 2021-01-23

Copyright © Ryan Kan

Description: The tests for the `questions` application.
"""

# IMPORTS
from datetime import timedelta

from django.utils.timezone import now
from django.test import TestCase, Client

from questions.models import Question

# CONSTANTS
INPUT_GENERATION_CODE_1 = """def input_generation():  # Copy the function signature EXACTLY
    # This is the input that will be shared for all users
    # Note that the formatting of the input is up to you; you just have to tell
    # the users the format of the input.
    input_ = "1, 2, 3, 4, 5, 6, 7"

    # This will be the answer for that input
    answer = "1234567"

    # Return BOTH strings
    return input_, answer"""

INPUT_GENERATION_CODE_2 = """def input_generation(seed_val=None):  # Copy the function signature EXACTLY
    # Import BUILT-IN libraries INSIDE the input generation function
    from random import randint, seed
    
    # Seed the PRNG
    seed(seed_val)
    
    # This is the input that will be generated for each user
    # NOTE: The input that is generated here is an INTEGER, not a string. So we
    #       must make it a string later.
    input_ = randint(-1000, 1000)

    # This is the solution code
    def solution(integer):
        # Simple function that determines whether the integer is greater than 0
        if integer > 0:
            return "YES"
        else:
            return "NO"

    # Generate the answer based on the generated input
    answer = solution(input_)

    # At this point, only the answer is a string. So we must also make the
    # input a string
    input_ = str(input_)  # Now it satisfies the requirements

    # Return BOTH strings
    return input_, answer"""


# TESTS
class QuestionsTests(TestCase):
    def setUp(self):
        # Create two questions, based on the sample questions in the `README.md` file
        Question.objects.create(title="Test 1",
                                short_description="Test 1 Short Description",
                                long_description="Test 1 Longer Description -- Is this long enough for you?",
                                input_generation_code=INPUT_GENERATION_CODE_1,
                                question_release_datetime=now(),
                                override_key="Test1Over")

        Question.objects.create(title="Test 2",
                                short_description="Test 2 Short Description",
                                long_description="Test 2 Longer Description -- Is this long enough for you?",
                                input_generation_code=INPUT_GENERATION_CODE_2,
                                question_release_datetime=(now() + timedelta(days=1)),
                                override_key="Test2Over")

        # Set up a fake test client
        self.client = Client()

    def test_descriptions(self):
        """Checks if the questions' descriptions were properly set."""

        # Get the question objects
        question1 = Question.objects.get(title="Test 1")
        question2 = Question.objects.get(title="Test 2")

        # Check short description
        self.assertEqual(question1.short_description, "Test 1 Short Description")
        self.assertEqual(question2.short_description, "Test 2 Short Description")

        # Check long description
        self.assertEqual(question1.long_description, "Test 1 Longer Description -- Is this long enough for you?")
        self.assertEqual(question2.long_description, "Test 2 Longer Description -- Is this long enough for you?")

    def test_input_generation(self):
        """Checks if the input generation code was executed correctly."""

        # Get the question objects
        question1 = Question.objects.get(title="Test 1")
        question2 = Question.objects.get(title="Test 2")

        # Execute `question1`'s input generation code
        temp = {}
        exec(question1.input_generation_code, temp)
        input_, answer = temp["input_generation"]()

        # Check if the input and answer are as expected
        self.assertEqual(input_, "1, 2, 3, 4, 5, 6, 7")
        self.assertEqual(answer, "1234567")

        # Execute `question2`'s input generation code
        temp = {}
        exec(question2.input_generation_code, temp)
        input_, answer = temp["input_generation"](seed_val=314159)

        # Check if the input and answer are as expected
        self.assertEqual(input_, "-607")
        self.assertEqual(answer, "NO")

    def test_question_release(self):
        """Checks if the question release code is working properly."""

        # Get the question objects
        question1 = Question.objects.get(title="Test 1")
        question2 = Question.objects.get(title="Test 2")

        # Check if they are released
        self.assertTrue(question1.is_question_released())  # Should have been released already
        self.assertFalse(question2.is_question_released())  # Should have NOT been released

    def test_ratelimit(self):
        """Checks if the ratelimit capabilities are working."""

        # Get the question object
        question = Question.objects.get(title="Test 1")  # We'll just need one

        # Get the question ID
        question1_id = question.id

        # Spam the question's url to exceed the ratelimit
        url = f"/questions/{question1_id}/"
        self.client.get(url)
        self.client.get(url)
        self.client.get(url)
        self.client.get(url)
        final_response = self.client.get(url)

        # Check if the page shows the 'plea' message
        self.assertTrue(str(final_response.content).count("Please do not") > 0)
