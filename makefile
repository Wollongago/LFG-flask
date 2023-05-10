.PHONY: up down logs test clear stop restart bash

export UID:=$(shell id -u)
export GID:=$(shell id -g)

default:
	@echo "Default target"

up:
	@echo "============= Sarting Webstack ============="
	@docker network inspect lfg-net >/dev/null || docker network create -d bridge --subnet 42.42.0.0/24 --gateway 42.42.0.1 lfg-net
	docker-compose -p lfg up -d

stop:
	@echo "============= Stopping http ============="
	docker-compose -p lfg stop flask-http

restart:
	@echo "============= Restart http ============="

	@LOGPATH=$$(docker inspect --format='{{.LogPath}}' lfg-flask-http-1); \
	if [ -n "$${LOGPATH}" ]; then sudo truncate -s 0 $${LOGPATH}; fi
	docker-compose -p lfg restart flask-http

reload:
	@echo "============= Reload http server ============="
	@docker exec -it $$(docker ps -aqf "name=lfg-flask-http-1") /bin/bash -c 'kill -HUP `cat /tmp/http.pid`'

down:
	@echo "============= Shutdown Everything ============="
	docker-compose -p lfg down --remove-orphans

logs:
	@echo "============= Logs of http ============="
	docker-compose -p lfg logs -f flask-http

bash:
	@echo "============= Entering Flask bash shell as $(UID):$(GID) ============="
	@docker exec --user $(UID):$(GID) -it $$(docker ps -aqf "name=lfg-flask-http-1") /bin/bash

build:
	@echo "============= Building http ============="
	test -n "$(VERSION)" # $$VERSION
	docker build --label lfg.flask.version=$(VERSION) \
	-t lfg-flask-http:$(VERSION) \
	-t lfg-flask-http:latest \
	-f Dockerfile .