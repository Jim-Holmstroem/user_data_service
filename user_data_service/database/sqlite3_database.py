from __future__ import print_function

from contextlib import closing

import uuid
import sqlite3

from ..utils import values
from database import ProtectableDatabase


class SQLite3Database(ProtectableDatabase):
    def __init__(
        self,
        database_name="users.db",
        uuid=lambda: uuid.uuid4().hex,
    ):
        self.uuid = uuid
        self.database_name = database_name

    def create(self, name, data, new_password_information=("", "")):
# FIXME if some of this doesn't exist .. (also at the level of password
# protected)
        with closing(self.conn.cursor()) as c:
            c.execute(
                "INSERT INTO users VALUES (?, ?, ?, ?, ?)",
                (
                    self.uuid(),
                    data["name"],
                    data["email"],
                ) +
                new_password_information
            )
            self.conn.commit()  # FIXME this must be commited

    def exists(self, name):
        with closing(self.conn.cursor()) as c:
            c.execute(
                "SELECT COUNT(*) FROM users WHERE name=?",
                (
                    name,
                )
            )
            count, = c.fetchone()
            exists = count > 0

            return exists

    def get(self, name):
        with closing(self.conn.cursor()) as c:
            c.execute(
                "SELECT id, name, email FROM users WHERE name=?",
                (
                    name,
                )
            )
            raw_data = c.fetchone()  # TODO raise understable exception in
                                     # case of missing (shouldn't occure here
                                     # but better safe then sorry)

            data = dict(zip(
                ("id", "name", "email"),
                raw_data
            ))

            return data

    def delete(self, name, data):
        with closing(self.conn.cursor()) as c:
            c.execute(
                "DELETE FROM users WHERE name=?",
                (
                    name,
                )
            )
            self.conn.commit()

    def update(self, name, data):
        valid_keys = {"email", "name"}
        valid_update_keys = set(data.keys()) & valid_keys
        if valid_update_keys:
            valid_update_values = values(valid_update_keys)(data)

            variable_definitions = ", ".join(
                map(
                    "{} = ?".format,
                    valid_update_keys
                )
            )
            update_queary_template = (
                "UPDATE users SET {variable_definitions}"
                "WHERE name=?"
            ).format(
                variable_definitions=variable_definitions
            )

            with closing(self.conn.cursor()) as c:
                c.execute(
                    update_queary_template,
                    valid_update_values + (name, )
                )
                self.conn.commit()  # FIXME this must be commited


    def _get_password_information(self, name):
        with closing(self.conn.cursor()) as c:
            c.execute(
                "SELECT password_hash, password_salt FROM users WHERE name=?",
                (
                    name,
                )
            )
            data = c.fetchone()

            return data

    def _set_password_information(self, name, password_information):
        with closing(self.conn.cursor()) as c:
            c.execute(
                (
                    "UPDATE users SET password_hash = ?, password_salt = ?"
                    "WHERE name=?"
                ),
                password_information + (name, )
            )
            self.conn.commit()  # FIXME this must be commited

    def connect(self):
        self.conn = sqlite3.connect(self.database_name)

    def close(self):
        self.conn.close()

    def init(self):
        schema = (  # users.sql
            "CREATE TABLE IF NOT EXISTS users("
                "id TEXT PRIMARY KEY NOT NULL,"
                "name TEXT NOT NULL UNIQUE,"
                "email TEXT NOT NULL,"
                "password_hash TEXT NOT NULL,"
                "password_salt TEXT NOT NULL"
            ")"  # TODO depends on PasswordProtectedDatabase structure
                 # (possible but currently too much work to break it out)
                 # also related to _get_password_information
        )
        with closing(self.conn.cursor()) as c:
            c.execute(schema)
            self.conn.commit()  # FIXME this must be commited
