from __future__ import print_function

from functools import wraps

from database import Database


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


class PrintDatabase(Database):
    @function_debug
    def create(self):
        pass
    @function_debug
    def read(self):
        pass
    @function_debug
    def update(self):
        pass
    @function_debug
    def delete(self):
        pass
