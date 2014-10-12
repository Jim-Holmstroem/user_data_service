#!/usr/bin/env python
from __future__ import print_function

from user_data_service.service import Service

from user_data_service.database.sqlite3_database import SQLite3Database
from user_data_service.database.password_protected import PasswordProtected
from user_data_service.database.valid import Valid
from user_data_service.endpoints import v0


if __name__ == '__main__':
    service = Service(
        database=Valid(PasswordProtected(SQLite3Database('data/users.db'))),
        endpoints=(v0,)
    )
    service.run(debug=True)
