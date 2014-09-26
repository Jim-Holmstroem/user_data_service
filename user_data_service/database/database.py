from __future__ import print_function

from abc import ABCMeta, abstractmethod


class Database(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def exists(self, name):
        pass

    @abstractmethod
    def create(self):
        pass

    @abstractmethod
    def read(self):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def delete(self):
        pass
