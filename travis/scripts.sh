#!/bin/bash -ex

# Authenticate to Docker (e.g. Docker Hub) to not reach the download rate limit when running in Travis CI
# see https://docs.travis-ci.com/user/docker/
# see https://docs.docker.com/docker-hub/download-rate-limit/
echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin

pipenv run invoke test
pipenv run invoke build
pipenv run invoke deploy ${1}
