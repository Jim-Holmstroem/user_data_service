run:
	./main.py

test:
	nosetests -sv

clean:
	find . -name "*.pyc" -delete

URL = localhost:5000/api/v0/users
NAME = test
NEWNAME = another
PASSWORD = abcd1234
NEWPASSWORD = abcd12345
CURLFLAGS = -s
LISTUSERS = sqlite3 data/users.db "SELECT * FROM users;"
PRE = "======= pre ==========\n`${LISTUSERS}`\n======================"
POST= "\n======= post =========\n`${LISTUSERS}`\n======================\n"

clear_database:
	rm data/users.db

try: try_post try_get try_get_specific try_patch_name try_patch_password try_delete

try_post:
	@echo ${PRE}
	curl ${CURLFLAGS} -H 'Content-Type: application/json' -d '{"name": "${NAME}", "email": "${NAME}@email.com", "password": "${PASSWORD}"}' -X 'POST' ${URL}
	@echo ${POST}

try_get:
	@echo ${PRE}
	curl ${CURLFLAGS} -X "GET" ${URL}
	@echo ${POST}

try_get_specific:
	@echo ${PRE}
	curl ${CURLFLAGS} -X "GET" ${URL}/${NAME}
	@echo ${POST}

try_patch_name:
	@echo ${PRE}
	curl ${CURLFLAGS} -H 'Content-Type: application/json' -d '{"name": "${NEWNAME}", "password": "${PASSWORD}"}' -X "PATCH" ${URL}/${NAME}
	@echo ${POST}

try_patch_password:
	@echo ${PRE}
	curl ${CURLFLAGS} -H 'Content-Type: application/json' -d '{"new_password": "${NEWPASSWORD}", "password": "${PASSWORD}"}' -X "PATCH" ${URL}/${NEWNAME}
	@echo ${POST}

try_delete:
	@echo ${PRE}
	curl ${CURLFLAGS} -H 'Content-Type: application/json' -d '{"password": "${NEWPASSWORD}"}' -X "DELETE" ${URL}/${NEWNAME}
	@echo ${POST}
