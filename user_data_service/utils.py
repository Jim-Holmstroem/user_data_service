from __future__ import print_function

from operator import methodcaller
from itertools import combinations, chain
from functools import wraps, partial

import json

from werkzeug.exceptions import default_exceptions, HTTPException
import flask
from flask import g

email = '{}@domain.com'.format


def database():
    return getattr(g, '_database', None)


class UserDataException(Exception):
    """UserDataException
    """


def password(name):
    return name[::-1]


def powerset(set_):
    return chain.from_iterable(
        map(
            partial(combinations, set_),
            range(len(set_) + 1)
        )
    )


def powerdict(dict_):
    return map(
        dict,
        powerset(dict_.items())
    )


def values(keys):
    def _values(sequence):
        data = tuple(map(sequence.__getitem__, keys))
        return data

    return _values


def always_json_response(application_prototype):
    """Wraps a Flask application to make it always return a JSON response.

    Parameters
    ----------
    application_prototype :: Flask.__class__

    Returns
    -------
    application_prototype_ :: Flask.__class__
    """
    @wraps(application_prototype)
    def application_prototype_(*args, **kwargs):
        def json_error(e):
            response = json_response(
                {
                    'message': str(e) if isinstance(e, HTTPException)
                        else "500: Internal Server Error"
                },
                pretty=True
            )
            response.status_code = e.code if isinstance(e, HTTPException)\
                else 500

            return response

        application = application_prototype(*args, **kwargs)

        register_errorhandlers = map(
            application.errorhandler,
            default_exceptions
        )
        map(
            methodcaller('__call__', json_error),
            register_errorhandlers
        )
        return application

    return application_prototype_


def json_response(dict_response, pretty=False, status_code=200):
    json_config = {'indent': 4} if pretty else {'indent': None}

    response = flask.Response(
        response=json.dumps(dict_response, **json_config),
        status=200,
        mimetype='application/json'
    )

    return response


def return_json(pretty=False):
    """
    Parameters
    ----------
    pretty :: bool
        If the return_json should be pretty or not.
    """
    def _return_json(f):
        """
        Parameters
        ----------
        dict_method :: *args, **kwargs -> dict
            A method returning a dict containing the wanted information.

        Returns
        -------
        response_method :: *args, **kwargs -> flask.Response
            Wraps the dict_method to instead return a flask.Response with
            proper mime etc.

        Note
        ----
        replacing flask.jsonify to go around an issue where flask.jsonify
        is using simplejson (as default import and json as fallback) with
        keyword argument indent.

        Note
        ----
        This is not header request nor flask config aware.
        """
        @wraps(f)
        def __return_json(*args, **kwargs):
            response = json_response(
                f(*args, **kwargs),
                pretty=pretty
            )

            return response

        return __return_json

    return _return_json
