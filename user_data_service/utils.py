from __future__ import print_function


from itertools import combinations, chain
from functools import wraps, partial

import json

import flask

email = '{}@domain.com'.format


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


def return_json(pretty=False):
    def _return_json(f):
        @wraps(f)
        def __return_json(self, **kwargs):
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
            pretty_json_config = {'indent': 4} if pretty else {'indent': None}
            return flask.Response(
                response=json.dumps(kwargs, **pretty_json_config),
                status=200,
                mimetype='application/json'
            )

        return __return_json

    return _return_json
