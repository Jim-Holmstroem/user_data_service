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
            raise Exception("Permission Denied")

        return f(self, name, data)

    return _password_protected


class PasswordProtected(Database):
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

    def exists(self, name):
        return self.database.exists(name)

    def get(self, name):
        return self.database.get(name)

    @password_protected
    def delete(self, name, data):
        hash_value, salt_value = self.database._get_password_information(name)
        if not self.valid(data["password"], hash_value, salt_value):
            raise Exception("Permission Denied")
        return self.database.delete(name)

    @password_protected
    def update(self, name, data):
        return self.database.update(name, data)

    def connect(self):
        return self.database.connect()

    def close(self):
        return self.database.close()

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
        print(self.hash_(password, salt_value))
        print(hash_value)
        return self.hash_(password, salt_value) == hash_value
