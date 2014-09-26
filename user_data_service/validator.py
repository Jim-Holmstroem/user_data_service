from __future__ import print_function


import re


def valid_name(name):
    """Validates a name.

    Arguments
    ---------
    name : str
        The name to validate

    Returns
    -------
    valid : bool
        Validity of the name
    """
    empty = len(name) == 0
    null = name == "null"

    valid = not (empty or null)

    return valid


def valid_password(password, minimum_length=8):
    """Validates a password.

    Arguments
    ---------
    password : str
        The password to validate

    Returns
    -------
    valid : bool
        Validity of the password
    """
    long_enough = len(password) >= minimum_length

    valid = long_enough

    return valid


def valid_email(email):
    """Validates an email.

    Note
    ----
    http://www.w3.org/TR/html5/forms.html#valid-e-mail-address

    Arguments
    ---------
    email : str
        The email to validate

    Returns
    -------
    valid : bool
        Validity of the email
    """
    valid_email_w3 = bool(re.match(
        pattern=r"^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]"
                "{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}"
                "[a-zA-Z0-9])?)*$",
        string=email
    ))

    valid = valid_email_w3

    return valid
