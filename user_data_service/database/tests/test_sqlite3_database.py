from __future__ import print_function


from nose.tools import (
    assert_equals,
    assert_not_equals,
    assert_true,
    assert_false,
)

from ..sqlite3_database import SQLite3Database
from ...utils import values


def email(name):
    return '{name}@domain.com'.format(name=name)


class test_SQLite3Database(object):
    def setup(self):
        self.db = SQLite3Database(':memory:')
        self.db.connect()

    def test_create_delete(self):
        def _test(name):
            original_data = {'name': name, 'email': email(name)}
            self.db.create(
                name,
                original_data
            )
            assert_true(self.db.exists(name))

            data = self.db.get(name)
            assert_equals(data["name"], name)
            assert_equals(data["email"], email(name))

            self.db.delete(name)
            assert_false(self.db.exists(name))

        _test('test')

    def test_update(self):
        def _test(name, updates):  # TODO combine yield and setup/teardown
            original_data = {'name': name, 'email': email(name)}
            self.db.create(
                name,
                original_data
            )
            self.db.update(name, updates)
            name_updated = "name" in updates
            (assert_true, assert_false)[name_updated](
                self.db.exists(name)
            )
            new_name = updates["name"] if name_updated else name
            data = self.db.get(new_name)
            updated_values = values(updates.keys())
            not_updated_values = values(
                set(original_data.keys()) - set(updates.keys())
            )
            map(
                assert_equals,
                updated_values(data),
                updated_values(updates),
            )
            map(
                assert_equals,
                not_updated_values(data),
                not_updated_values(original_data),
            )
            self.db.delete(new_name)

        _test('test', {'name': 'somethingelse'})
        _test('test', {'email': 'me@domain.org'})
        _test('test', {'name': 'somethingelse', 'email': 'me@domain.org'})

    def teardown(self):
        self.db.close()
