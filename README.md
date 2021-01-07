# Quaestiones
 An application that assists you in making a simple questions asking site.

# Making a Question
## Writing the Description of the Question
The description of the question is the heart of the question itself. Without a good description, the users would likely be confused or unsure on how to proceed.

The description of the question should be **written in the Markdown language**. A guide to the Markdown language can be found [here](https://www.markdownguide.org/), and a helpful cheatsheet can also be found [here](https://www.markdownguide.org/cheat-sheet/). 

Here are the basics of Markdown:
* Headings in Markdown are written using the hash `#` symbol. The higher the number of hashes, the **smaller** the heading will be. For example, `# Hello` is the largest heading, while `## Hello` is a slightly smaller heading. Note that Quaestiones' largest heading is the `##` heading.
* To emphasise a piece text, type `*Your text here*`. For example, *to put emphasis here*, type `*to put emphasis here*`.
    * **Note: Bolded words will not render correctly in the Quaestiones website, so do not use them.**
* To make a list, either prepend `*`, `-` or a number followed by a dot (e.g. `1.`, `2.`) in front of a line. For example, `* First bullet point`, `- Second bullet point`, `1. First ordered point`.
* To type code, surround your text with backticks `` ` ``. For example `` `This will be rendered as code` `` will be shown as `This will be rendered as code`.
    * To make a large section of text code, type ` ``` ` before and after a section of text.
* To add a link, type `[What will be shown](The underlying link)`. For example, `[Example Domain](https://example.com/)` will be shown as [Example Domain](https://example.com/), with `Example Domain` being clickable.
* To strikethrough a section of text, type `~~` before and after the text. For example, `~~This will be striked~~` will be shown as ~~This will be striked~~.
* To add hidden text which can only be revealed after you hover your mouse's cursor on the text, type `<span title="Hidden text here">Main text here</span>`.

***Note: Images are not officially supported by the Quaestiones Markdown Parsing System.***

The full description of the question would likely use a combination of most or all of these elements. It is also possible that your question's description would use none of the above Markdown elements. All that matters is that **your question's descripion is clear and easily understandable**.

## Input Generation Code
When you are making a question, you would often want to provide the question's input to the user. This can be done though the questions' management portal.

When editing a question, one of the fields would be `Input Generation Code`. This field is mandatory, and the input of that field **must follow the following rules**.

First, the code that is in the `Input Generation Code` field **must be in Python 3.8**. This is because the parser of the code will also be in Python 3.8.
(Note: code from other versions of Python 3 would *likely* be acceptable, however code written in Python 3.9 or later or code written in Python 2 would **not be accepted**.)

Next, the Input Generation Code must contain the line:
```python
def input_generation():
    # Write your code here
```
This is because the server will call this function to generate the input for the users. Note that **the input for every user can be the same**. It is optional to make it different for every user, but **it is supported**.

Next, the `input_generation` function **must only use built-in python libraries**.

Finally, the `input_generation` function **must return the following two things, in the same order as specified here**:
* **A string** which is the input for the puzzle.
* **Another string** which is the answer for the given input.

This implies that your solution code **must also be contained inside the `input_generation` function**, so that the correct answer can be generated at the same time as the generation of the input.
(Note: this means that your solution code **must be efficient**.)

Here are some examples:
* The following code **provides the same input** for all users:
```python
def input_generation():  # Copy the function signature EXACTLY
    # This is the input that will be shared for all users
    # Note that the formatting of the input is up to you. You just have to tell
    # the users the input's format.
    input_ = "1, 2, 3, 4, 5, 6, 7"

    # This will be the answer for that input
    answer = "1234567"

    # Return BOTH strings
    return input_, answer
```
* The following code **generates pseudo-random quasi-unique inputs** for every user:
```python
def input_generation():  # Copy the function signature EXACTLY
    # Import BUILT-IN libraries INSIDE the input generation function
    from random import randint

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
    return input_, answer
```

You may check your own input generation code using the `Check Input Generation Code.py` file that is in the `Other Files` directory.

**TL;DR**:
* Input must be in **Python 3.8**
* The first line must contain `def input_generation()`
* The `input_generation` function **must only use built-in python libraries**.
* The function must return two things:
    * **A string** which is the input for the puzzle
    * **Another string** which is the correct answer for the puzzle
