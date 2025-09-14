YEARS ?= 2020 2021

.PHONY: build up server client down clean

build:
	docker-compose build

server:
	docker-compose up -d movie-server

client:
	docker-compose run --rm movie-client --server http://movie-server:8080 $(YEARS)

up:
	docker-compose up -d

down:
	docker-compose down

clean:
	docker-compose down -v --rmi all

