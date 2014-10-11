run:
	./main.py

test:
	nosetests -sv

clean:
	find . -name "*.pyc" -delete

URL = localhost:5000/api/v0/users
USER = test
PASSWORD = abc123
CURLFLAGS = -s

try: try_post try_get try_get_specific try_delete try_patch_name try_patch_password

try_post:
	curl ${CURLFLAGS} -H 'Content-Type: application/json' -d '{"name": "${USER}", "email": "${USER}@email.com", "password": "${PASSWORD}"}' -X 'POST' ${URL}
	@echo ""

try_get:
	curl ${CURLFLAGS} -X "GET" ${URL}
	@echo ""

try_get_specific:
	curl ${CURLFLAGS} -X "GET" ${URL}/${USER}
	@echo ""

try_delete:
	curl ${CURLFLAGS} -H 'Content-Type: application/json' -d '{"password": "${PASSWORD}"}' -X "DELETE" ${URL}/${USER}
	@echo ""

try_patch_name:
	curl ${CURLFLAGS} -H 'Content-Type: application/json' -d '{"name": "another", "password": "${PASSWORD}"}' -X "PATCH" ${URL}/${USER}
	@echo ""

try_patch_password:
	curl ${CURLFLAGS} -H 'Content-Type: application/json' -d '{"new_password": "abc234", "password": "${PASSWORD}"}' -X "PATCH" ${URL}/${USER}
	@echo ""
