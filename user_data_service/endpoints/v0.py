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

    # TODO use flask.jsonify instead see utils.return_json for more information
    @return_json(pretty)
    def get(self, name=None):
        return dict(
            name=name,
        )

    @return_json(pretty)
    def post(self):
        return dict(
            a="posted",
        )

    @return_json(pretty)
    def delete(self, name):
        return dict(
            a='delete',
            name=name,
        )

    @return_json(pretty)
    def patch(self, name):
        return dict(
            a='patch',
            name=name,
        )


def install(application):
    register_user_endpoint(application, UserAPIv0, 'v0')
