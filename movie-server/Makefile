OUTPUT := movie-server
default: install

build:
	@go generate
	@go build -o $(OUTPUT)

install:
	@go generate
	@go install

.PHONY: build install
