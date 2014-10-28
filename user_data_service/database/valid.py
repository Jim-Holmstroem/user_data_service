from __future__ import print_function

from operator import and_
from functools import wraps

import re


def valid_name(name):
    """Validates a name.  Arguments ---------
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


def valid(data):
    name_valid = valid_name(data["name"]) if "name" in data\
        else True
    email_valid = valid_email(data["email"]) if "email" in data\
        else True
    password_valid = valid_password(data["password"]) if "password" in data\
        else True
    new_password_valid = valid_password(data["new_password"]) if "new_password" in data\
        else True

    data_valid = reduce(
        and_,
        [
            name_valid,
            email_valid,
            password_valid,
            new_password_valid,
        ]
    )

    return data_valid


def valid_protected(f):
        @wraps(f)
        def _valid_protected(self, name, data):
            if not valid(data):
                raise Exception('Invalid data')  # TODO make it more specific
            return f(self, name, data)
        return _valid_protected


class Valid(object):  # TODO .(Database)
    def __init__(self, database):
        self.database = database

    @valid_protected
    def create(self, name, data):
        return self.database.create(name, data)

    @valid_protected
    def update(self, name, data):
        return self.database.update(name, data)

    def __getattr__(self, attribute_name):
        return getattr(self.database, attribute_name)
