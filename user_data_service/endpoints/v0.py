from __future__ import print_function

from flask import views, request, g
from werkzeug.exceptions import HTTP_STATUS_CODES, HTTPException

from ..utils import return_json, database


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
    def get(self, name):
        if g._database.exists(name):
            data = g._database.get(name)

            return dict(
                data=data,
            )

        else:
            raise HTTPException(HTTP_STATUS_CODES[404], 404)

    @return_json(pretty)
    def post(self):
        data = request.get_json()
        g._database.create(data["name"], data)

        return dict()

    @return_json(pretty)
    def delete(self, name):
        data = request.get_json()
        g._database.delete(name, data)

        return dict()

    @return_json(pretty)
    def patch(self, name):
        data = request.get_json()
        g._database.update(name, data)

        return dict()


def install(application):
    register_user_endpoint(application, UserAPIv0, 'v0')
