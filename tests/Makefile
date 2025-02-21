# Makefile

IMAGE_NAME := explainbrainroi
CONTAINER_NAME := explainbrainroi-streamlit

all: build run

build:
	docker build -t $(IMAGE_NAME) .

run:
	docker run -d  --rm -p 8501:8501 -v .:/app --name $(CONTAINER_NAME) $(IMAGE_NAME)

restart: stop run

stop:
	docker stop $(CONTAINER_NAME) || true
	docker rm $(CONTAINER_NAME) || true

.PHONY: all build run restart stop
