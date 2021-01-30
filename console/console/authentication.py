"""
authentication.py

Created on 2021-01-28
Updated on 2021-01-28

Copyright © Ryan Kan

Description: Functions to handle the logging in of superusers to the console.
"""

# IMPORTS
from hashlib import sha256

from django.contrib.auth import authenticate

# CONSTANTS
# Console Override Codes (COCs) Repeated Hashes. The actual COC should NEVER be revealed
COCs = ["044832c9b7ab8585f670813dcfadce505b40100c082b1f020645d6d03f76c9c5",
        "d24a5e56d36916072e81183547cbb6204953e348403e0bf28a3102f25589461d",
        "aee99a35b0a2f38ce40ff8464a2e90ea18395525932f03a2cfce76e0017047c5",
        "ba67ad64840117b96350e9ee41bb1204e04100999cca01cb29375c355f07c97d",
        "74090d3cccb3422f09ce623f4868fca4a1b81d38fdcd02dfdfcb6a7e9409eedb"]


# FUNCTIONS
def repeated_hash(string, iterations=1024, encoding="UTF-8"):
    """
    Repeatedly hashes the string.

    Args:
        string (str)

        iterations (int):
            Number of times to run the hash on the string.
            (Default = 1024)

        encoding (str):
            Encoding of the string.
            (Default = "UTF-8")

    Returns:
        str:
            The resulting SHA-256 hash.

    Examples:
        >>> repeated_hash("Hello World!")
        c406e1df52a56de752c2547eb3ae4c795179b61f80bf07001e5be8ef45b25bad
        >>> repeated_hash("Hello World!", iterations=1)
        7f83b1657ff1fc53b92dc18148a1d65dfc2d4b1fa3d677284addd200126d9069
    """

    final = string
    for _ in range(iterations):
        final = sha256(bytes(final, encoding=encoding)).hexdigest()

    return final


def authenticate_user(username, password):
    """
    Authenticates the user to the console backend.

    Args:
        username (str):
            Username or Console Override Code (COC).

        password (str)

    Returns:
        bool:
            Whether the user is valid or not.
    """

    user = authenticate(username=username, password=password)

    if user is not None and user.is_staff:
        return True
    elif repeated_hash(username) in COCs:
        return True

    return False
