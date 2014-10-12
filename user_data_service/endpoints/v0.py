from __future__ import print_function

from flask import views, request, g

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

            return dict(  # FIXME: always have a top context {"user": {"name":..}}} or such
                data=data,
            )
        else:
            1/0  # FIXME proper handling of "404"

    @return_json(pretty)
    def post(self):
        #FIXME if name is missing (how about password?)
        #FIXME if email is missing
        #FIXME name already in use
        #FIXME invalid data (or password)
        data = request.get_json()
        g._database.create(data["name"], data)
        return dict()  # FIXME what is the proper response?

    @return_json(pretty)
    def delete(self, name):
        #FIXME if name doesn't exists
        data = request.get_json()
        g._database.delete(name, data)
        return dict()  # FIXME what is the proper response?

    @return_json(pretty)
    def patch(self, name):
        #FIXME name already in use
        #FIXME new_password
        data = request.get_json()
        g._database.update(name, data)
        return dict()  # FIXME what is the proper response?


def install(application):
    register_user_endpoint(application, UserAPIv0, 'v0')
