# Quaestiones
An application that assists you in making a simple questions asking site.

# Setup
You will need to have [**Python 3.8**](https://www.python.org/downloads/release/python-386/) installed for this software to work.

1. Download either:
    - the latest release of Quaestiones;
    - [the latest stable development build](https://github.com/Ryan-Kan/Quaestiones/archive/main.zip); or
    - [the current development version](https://github.com/Ryan-Kan/Quaestiones/archive/Development.zip)

## Setting Up the Project Folder
2. Extract the contents of the `zip` file into an empty folder. Let's call that folder the *Root Directory*. Rename the *Root Directory* as `Quaestiones`.
    - The root directory should have a project structure similar to the following (not all files and folders are shown):
```
Quaestiones
├── Assets
├── LICENSE
├── Other Files
├── Quaestiones
│   ├── asgi.py
│   ├── settings
│   │   ├── __init__.py
│   │   ├── common.py
│   │   ├── development.py
│   │   ├── production.py
│   │   └── quaestiones.py
│   ├── templates
│   │   ├── Quaestiones
│   │   ├── admin
│   │   └── global
│   ├── urls.py
│   └── views.py
├── README.md
├── Todos.txt
├── accounts
├── manage.py
├── misc
├── questions
├── requirements.txt
└── stats
```
3. Inside the *Root Directory*, you should see a folder named `Quaestiones`. Navigate into that folder.
4. Create a new folder inside `Quaestiones` with the name `SecretFiles`.
5. Inside `SecretFiles`, create two files:
    a. `secret.txt`
    b. `email_credentials.yaml`
6. Now the project structure should look something like this (not all files and folders are shown):
```
Quaestiones
└── Quaestiones
    └── SecretFiles
        └── secret.txt
        └── email_credentials.yaml
```
7. Run the following command and then copy & paste its output into `secret.txt`:
```bash
base64 /dev/urandom | head -c50; echo
```
8. a. Copy and paste the following content into `email_credentials.yaml`:
```yaml
email_use_tls: true
email_host: SMTP_SERVER_HOST
email_user: EMAIL_ADDRESS
email_password: EMAIL_PASSWORD
email_port: SMTP_SERVER_PORT
```
8. b. **Note**: If you are using the GMail SMTP server, then [follow this guide](https://dev.to/abderrahmanemustapha/how-to-send-email-with-django-and-gmail-in-production-the-right-way-24ab) (especially the section titled "The Gmail part ✉") and thereafter copy and paste this content instead:
```yaml
email_use_tls: true
email_host: smtp.gmail.com
email_user: YOUR_GMAIL_ADDRESS
email_password: YOUR_APP_PASSWORD_FOR_QUAESTIONES
email_port: 587
```
9. Fill in the fields inside `email_credentials.yaml`.
10. Navigate back to the *Root Directory*.
11. Create the following three folders inside the *Root Directory*. These three folders are to **be kept empty**.
    - `Logs`
    - `StaticFiles`
    - `MediaFiles`

## Setting Up the Server Environment
**Note**: For all commands with `python`, if they do not work, **replace `python` with `python3`**. If they still do not work, **contact the project maintainer(s)**.

12. While inside the *Root Directory*, create a *Virtual Environment* (venv). To do so, run:
```bash
python -m venv venv --prompt Quaestiones
```
13. Activate the venv by running:
```bash
source venv/bin/activate
```
14. Check that your command line looks something like the following (emphasis on the `Quaestiones` in between the brackets):
```
(Quaestiones) User Quaestiones % 
```
15. Install all the project requirements by running
```
python -m pip install -r requirements.txt
```

# Files You Can Edit
Quaestiones has been made to ensure maximum customability with minimal editing of many different files. As such, it is essential that **you edit files that can be edited**. This is because the editing of files other than those permitted here **may result in unwanted side effects**, and **any support for your specific software will not be granted**.

The following are the files and/or directories that you may edit. All of these files/directories are with reference to the *Root Directory* (i.e. the *Root Directory* is not written on any of these paths).
- `accounts/templates/accounts/emails`
- `Logs`
- `MediaFiles`
- `Other Files`
- `Quaestiones/SecretFiles`
- `Quaestiones/settings`
- `Quaestiones/templates`
- `README.md`
- `StaticFiles`
- `stats/scoring.py`
- `Todos.txt`
- All `urls.py` files

# Making a Question
## Writing the Description of the Question
The description of the question is the heart of the question itself. Without a good description, the users would likely be confused or unsure on how to proceed.

The description of the question should be **written in the Markdown language**. A guide to the Markdown language can be found [here](https://www.markdownguide.org/), and a helpful cheatsheet can also be found [here](https://www.markdownguide.org/cheat-sheet/). 

***Note: Images are not officially supported by the Quaestiones Markdown Parsing System.***

The full description of the question would likely use a combination of Markdown elements. Regardless whether Markdown was used, ensure that **your question's descripion is clear, unambiguous, and easily understandable**.

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
