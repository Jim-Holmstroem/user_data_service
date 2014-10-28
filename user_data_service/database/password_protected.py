from __future__ import print_function

from functools import wraps

import hashlib
import uuid

from database import Database


def password_protected(f):
    @wraps(f)
    def _password_protected(self, name, data):
        password_information = self.database._get_password_information(name)
        if not self.valid(data["password"], *password_information):
            raise Exception("Permission Denied")  # FIXME is this something else then 500 internal server?

        return f(self, name, data)

    return _password_protected


class PasswordProtected(object):  # FIXME .(ProtectableDatabase)? (how to deal with Valid together with Database/PasswordProtectableDatabase)
    """Higher order database, takes a database and returns a password
    protected one.

    Arguments
    ---------
    salt :: () -> salt_value
        A salt factory.

    hash_ :: password, salt_value -> hash_value
        Generates the salted hash.
    """
    def __init__(
        self,
        database,
        salt=lambda: uuid.uuid4().hex,
        hash_=lambda w, salt: hashlib.sha512(w + salt).hexdigest(),
        # TODO use Passlib which uses PBKDF2
        # (rule #1 in security: never make your own)
    ):
        self.database = database
        self.salt = salt
        self.hash_ = hash_

    def create(self, name, data):
        return self.database.create(
            name,
            data,
            new_password_information=self.password_information(
                data["password"]
            )
        )

    @password_protected
    def delete(self, name, data):
        return self.database.delete(name, data)

    @password_protected
    def update(self, name, data):
        if "new_password" in data:
            self._set_password_information(
                name,
                self.password_information(data["new_password"])
            )

        return self.database.update(name, data)

    def __getattr__(self, attribute_name):  # TODO Metaclass: Wrapper(wrapped_name)  return getattr(getattr(self, wrapped_name), attribute_name)
        return getattr(self.database, attribute_name)

    def password_information(
        self,
        password,
        salt=None,
        hash_=None,
    ):
        """Creates a hash, salt pair from the password

        Attributes
        ----------
        password : str
            The password to secure.

        Returns
        -------
        hash_value, salt_value : str, str
            The hashed password and the salt used in hex strings.
        """
        salt = self.salt if salt is None else salt
        hash_ = self.hash_ if hash_ is None else hash_

        salt_value = salt()

        hash_value = hash_(password, salt_value)

        return hash_value, salt_value

    def valid(
        self,
        password,
        hash_value,
        salt_value
    ):
        password_hash_value = self.hash_(password, salt_value)
        password_valid = (password_hash_value == hash_value)

        return password_valid
