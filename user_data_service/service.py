from __future__ import print_function

from operator import methodcaller
from flask import Flask


from endpoints import v0


class Service(object):
    def __init__(self, endpoints=(v0,)):
        self.application = Flask("user_data_service")
        self.endpoints = endpoints

    def run(self, *args, **kwargs):
        map(
            methodcaller('install', self.application),
            self.endpoints
        )

        return self.application.run(*args, **kwargs)
