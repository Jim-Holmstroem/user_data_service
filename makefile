run:
	./main.py

test:
	nosetests -sv


URL = localhost:5000/api/v0/users
USER = test

try: try_post try_get try_get_specific try_delete try_patch

try_post:
	curl -s -X "POST" ${URL}
	@echo ""

try_get:
	curl -s -X "GET" ${URL}
	@echo ""

try_get_specific:
	curl -s -X "GET" ${URL}/${USER}
	@echo ""

try_delete:
	curl -s -X "DELETE" ${URL}/${USER}
	@echo ""

try_patch:
	curl -s -X "PATCH" ${URL}/${USER}
	@echo ""
