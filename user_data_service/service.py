from __future__ import print_function

from operator import methodcaller

from flask import Flask, g

from utils import always_json_response
from database.sqlite3_database import SQLite3Database
from database.password_protected import PasswordProtected
from endpoints import v0


class Service(object):
    def __init__(
        self,
        database=SQLite3Database(':memory:'),
        endpoints=(v0,)
    ):
        self.application = always_json_response(Flask)("user_data_service")
        self.endpoints = endpoints
        self.database = database

    def run(self, *args, **kwargs):
        def init_database():
            print('init')
            self.database.connect()
            self.database.init()

        def setup_database():
            self.database.connect()
            g._database = self.database

        def teardown_database(exception):
            database = getattr(g, '_database', None)
            if database is not None:
                database.close()

        self.application.before_first_request(init_database)
        self.application.before_request(setup_database)
        self.application.teardown_request(teardown_database)

        map(
            methodcaller('install', self.application),
            self.endpoints
        )

        return self.application.run(*args, **kwargs)
