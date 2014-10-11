from __future__ import print_function

from abc import ABCMeta, abstractmethod


class Database(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def exists(self, name):
        pass

    @abstractmethod
    def create(self, name, data):
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

    @abstractmethod
    def init(self):
        pass


class ProtectableDatabase(Database):
    @abstractmethod
    def create(self, name, data, new_password_information=("", "")):
        pass

    @abstractmethod
    def delete(self, name, data):
        pass

    @abstractmethod
    def _get_password_information(self, name):
        pass

    @abstractmethod
    def _set_password_information(self, name, password_information):
        pass
