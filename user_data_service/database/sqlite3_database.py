from __future__ import print_function

import uuid


from contextlib import closing
import sqlite3
from database import Database


class SQlite3Database(Database):
    def __init__(self,
        database_name="users.db",
        uuid=lambda: uuid.uuid4().hex,
    ):
        self.uuid = uuid
        self.conn = sqlite3.connect(database_name)
        schema_setup = "CREATE TABLE IF NOT EXISTS users("
            "id TEXT PRIMARY KEY NOT NULL,"  # TODO char(N)
            "name TEXT NOT NULL UNIQUE,"
            "email TEXT NOT NULL,"
            "password_hash TEXT NOT NULL,"  # TODO depends on PasswordProtectedDatabase structure (possible but currently too much work to break it out)
            "password_salt TEXT NOT NULL"
        ")"
        with closing(self.conn.cursor()) as c:
            c.execute(schema_setup)

    def create(self, name, data, new_password_information=("", "")):
        with closing(self.conn.cursor()) as c:
            c.execute(
                "INSERT INTO users (?, ?, ?, ?, ?)",
                (
                    self.uuid(),
                    data["name"],
                    data["email"],
                ) +\
                new_password_information
            )

    def exists(self, name):
        with closing(self.conn.cursor()) as c:

    def get(self, name):
        with closing(self.conn.cursor()) as c:

    def delete(self, name):
        with closing(self.conn.cursor()) as c:

    def update(self, name, data):
        with closing(self.conn.cursor()) as c:

    def _get_password_information(self, name):  # TODO depends on PasswordProtectedDatabase structure (possible but currently too much work to break it out)
        with closing(self.conn.cursor()) as c:

    def close(self):
        self.conn.close()
