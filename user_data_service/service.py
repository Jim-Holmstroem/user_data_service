from __future__ import print_function

from operator import methodcaller

from flask import Flask, g

from utils import always_json_response


class Service(object):
    def __init__(
        self,
        database,
        endpoints
    ):
        self.application = always_json_response(Flask)("user_data_service")
        self.endpoints = endpoints
        self.database = database

    def run(self, *args, **kwargs):
        def init_database():
            self.database.connect()
            self.database.init()  # FIXME :memory: returns new after each "connect"

        def setup_database():  # TODO verify thread safe?
            self.database.connect()  # FIXME fix this with proper context etc
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
