from __future__ import print_function

from flask import views

from ..utils import return_json


def register_user_endpoint(application, method_view, version):
    prefix = '/api/{version}/users'.format(version=version)
    user_view = method_view.as_view('user_api')

    application.add_url_rule(
        '{prefix}'.format(prefix=prefix),
        view_func=user_view,
        methods=['POST', ]
    )
    application.add_url_rule(
        '{prefix}/<string:name>'.format(prefix=prefix),
        defaults={'name': None},
        view_func=user_view,
        methods=['GET', ]
    )
    application.add_url_rule(
        '{prefix}/<string:name>'.format(prefix=prefix),
        view_func=user_view,
        methods=['PATCH', 'DELETE']
    )


class UserAPIv0(views.MethodView):
    pretty = True

    @return_json(pretty)
    def get(self, name=None):
        return self.__class__.jsonify_user(
            a='test'
        )

    @return_json(pretty)
    def post(self):
        return {'a': 'something'}

    @return_json(pretty)
    def delete(self, name):
        return {'a': 'simple_delete'}

    @return_json(pretty)
    def patch(self, name):
        return {'a': 'simple_patch'}


def install(application):
    register_user_endpoint(application, UserAPIv0, 'v0')
