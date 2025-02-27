# environment variables for the commands (docker compose, poetry)
export COMPOSE_PROJECT_NAME := e2e
export PORT_REVERSE_PROXY := 9000
export MONGO_PORT := 27050
export QUEUE_SLEEP_TIME := 1
export COMMON_HF_ENDPOINT := https://hub-ci.huggingface.co
export COMMON_HF_TOKEN := hf_app_datasets-server_token
export PARQUET_AND_DATASET_INFO_COMMITTER_HF_TOKEN := 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
export API_UVICORN_PORT := 9080
export ADMIN_UVICORN_PORT := 9081
export FIRST_ROWS_MAX_NUMBER := 4
export PROMETHEUS_MULTIPROC_DIR := /tmp
export ADMIN_UVICORN_NUM_WORKERS := 2
export API_UVICORN_NUM_WORKERS := 2
export COMMON_LOG_LEVEL := DEBUG

# makefile variables
DOCKER_COMPOSE := ../tools/docker-compose-datasets-server.yml
DOCKER_IMAGES := ../chart/docker-images.yaml

include ../tools/Python.mk
include ../tools/PythonTest.mk
include ../tools/DockerRemoteImages.mk
include ../tools/Docker.mk

.PHONY: e2e
e2e:
	make test

.PHONY: openapi
openapi:
	poetry run python -m openapi_spec_validator ../chart/static-files/openapi.json
