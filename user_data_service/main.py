#!/usr/bin/env python
from __future__ import print_function

from functools import wraps
from flask import Flask, json, views

app = Flask(__name__)


def return_json(f):
    @wraps(f)
    def _return_json(*args, **kwargs):
        return json.dumps(
            f(*args, **kwargs)
        )

    return _return_json


class User(views.MethodView):
    def get(self, name):
        return 'simple {}'.format(name)

    def put(self, name):
        return 'simple_put'

    def post(self):  # FIXME, post one send the name here??
        return 'simple_post'

    def delete(self, name):
        return 'simple_delete'

    def patch(self, name):
        return 'simple_patch'


app.add_url_rule('/api/v1/users/<string:name>', view_func=User.as_view('user'))


if __name__ == '__main__':
    app.run(debug=True)
