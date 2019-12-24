.SUFFIXES:

IMAGE?=cfstep

.PHONY: all
all: build run

.PHONY: build
build:
	@docker build . -t $(IMAGE)

.PHONY: run
run:
	@docker run -it --rm $(IMAGE)
