from __future__ import print_function


from itertools import combinations, chain
from functools import wraps, partial

from flask import json


email = '{}@domain.com'.format


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


def return_json(f):
    @wraps(f)
    def _return_json(*args, **kwargs):
        return json.dumps(
            f(*args, **kwargs)
        )

    return _return_json
