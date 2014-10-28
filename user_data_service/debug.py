from __future__ import print_function

from functools import wraps


def function_debug(f):
    @wraps(f)
    def _function_debug(*args, **kwargs):
        print('{fname}(\n{args},\n{kwargs}\n)\n'.format(
            fname=f.__name__,
            args=args,
            kwargs=kwargs,
        ))
        return f(*args, **kwargs)

    return _function_debug
