from __future__ import print_function

import hashlib
import uuid

from database import Database


class PasswordProtectedDatabase(Database):
    """Higher order database, takes a database and returns a password
    protected one.

    Arguments
    ---------
    salt :: () -> salt_value
        A salt factory.

    hash_ :: password, salt_value -> hash_value
        Generates the salted hash.
    """
    def __init__(self,
        database,
        salt=lambda: uuid.uuid4().hex,
        hash_=lambda w, salt: hashlib.sha512(w + salt).hexdigest(),
    ):
        self.database = database
        self.salt = salt
        self.hash_ = hash_

    def create(self, data):
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

    def delete(self, name):
        # FIXME no password check..
        return self.database.delete(name)

    def update(self, data):
        # FIXME no password check..
        password_information(password, salt=lambda: salt_value) == self.database._get_password_informamtion(name)
        return self.update(data)

    def _get_password_informamtion(self, name):
        return self.database._get_password_informamtion(name)


    def password_information(self,
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


    def validate(self,
        password,
        hash_value,
        salt_value
    ):
        pass
