from __future__ import print_function

from flask import Flask, views

from utils import return_json


app = Flask("user_data_service")


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
