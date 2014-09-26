from __future__ import print_function

from database import Database


class PasswordProtectedDatabase(Database):
    """Higher order database
    """
    def __init__(self,
        database,

    ):
        pass

    def (self,
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
