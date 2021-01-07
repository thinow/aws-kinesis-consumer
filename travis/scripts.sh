#!/bin/bash -ex

# Authenticate to Docker (e.g. Docker Hub) to not reach the download rate limit when running in Travis CI
# see https://docs.travis-ci.com/user/docker/
# see https://docs.docker.com/docker-hub/download-rate-limit/
echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin

# Automated test
pipenv run invoke test

# Build distribution package
pipenv run invoke dist

# Publish to https://test.pypi.org/
pipenv run pip install twine==3.2.0
pipenv run twine upload --skip-existing --repository-url https://test.pypi.org/legacy/ dist/*
