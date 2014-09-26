from __future__ import print_function

from flask import json

import hashlib
import uuid

from functools import wraps


def return_json(f):
    @wraps(f)
    def _return_json(*args, **kwargs):
        return json.dumps(
            f(*args, **kwargs)
        )

    return _return_json
