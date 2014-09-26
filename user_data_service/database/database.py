from __future__ import print_function

from abc import ABCMeta


class Database(object):
    __metaclass__ = ABCMeta

    def create(self):
        pass
    def read(self):
        pass
    def update(self):
        pass
    def delete(self):
        pass
