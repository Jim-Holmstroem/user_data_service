from __future__ import print_function

import uuid

from database import Database


class PasswordHandler(object):
    def secure_password(self,
        password,
        salt=lambda: uuid.uuid4().hex,
        hash_=lambda w, salt: hashlib.sha512(w + salt).hexdigest()
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
        salt_value = salt()

        hash_value = hash_(password, salt_value)

        return hash_value, salt_value


    def validate(self,
        password,
        hash_value,
        salt_value
    ):
        pass

class SQlite3Database(Database):
    def __init__(self,
        directory="users.db",
        uuid=lambda: uuid.uuid4().hex,
    ):
        self.uuid = uuid()
        create_table_query = "CREATE TABLE IF NOT EXISTS users("
            "id char(32) NOT NULL,"
            "name TEXT NOT NULL,"
            "email TEXT NOT NULL,"
            "password_hash char(128) NOT NULL,"
            "password_salt char(32) NOT NULL"
        ")"

    def create(self, data):
        c.execute(
            "INSERT INTO users (?, ?, ?, ?, ?)",
            (
                self.uuid(),
                data...
            )
        )

    def exists(self, name):
        pass

    def get(self, name):
        pass

    def delete(self, name):
        pass

    def update(self, data):
        pass
