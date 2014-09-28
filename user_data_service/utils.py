from __future__ import print_function

from flask import json

from functools import wraps


def values(keys):
    def _values(sequence):
        data = tuple(map(sequence.__getitem__, keys))
        return data

    return _values


def return_json(f):
    @wraps(f)
    def _return_json(*args, **kwargs):
        return json.dumps(
            f(*args, **kwargs)
        )

    return _return_json
