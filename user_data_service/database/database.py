from __future__ import print_function

from abc import ABCMeta, abstractmethod


class Database(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def exists(self, name):
        pass

    @abstractmethod
    def create(self, name):
        pass

    @abstractmethod
    def get(self, name):
        pass

    @abstractmethod
    def update(self, name, data):
        pass

    @abstractmethod
    def delete(self, name):
        pass

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def close(self):
        pass
