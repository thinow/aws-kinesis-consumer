# Contributing to aws-kinesis-consumer

First, thanks for taking interest in contributing to this application ! This is highly appreciated ! 🤗

You will find here some guidelines to help you start contributing to `aws-kinesis-consumer`.

## Install

To run the application, the machine needs to have the following being installed :

1. [Git](https://git-scm.com/downloads)
1. [Docker](https://www.docker.com/get-started)
1. [Python (version 3.6 or greater)](https://www.python.org/downloads/)
1. [Pipenv](https://pipenv.pypa.io/en/latest/#install-pipenv-today)

After all the requirements have been installed, the source code of `aws-kinesis-consumer` can be downloaded and
initialised :

```shell
git checkout https://github.com/thinow/aws-kinesis-consumer.git

cd aws-kinesis-consumer

# install the dependencies of aws-kinesis-consumer
pipenv sync --dev
```

Congrats! From now on, you are able to run the tests and the application from your machine.

## Run the tests

Run the following command. Here is an example of the expected output :

```shell
$ pipenv run invoke test

Starting aws-kinesis-consumer_kinesis_1 ... done
============================= test session starts ==============================
platform darwin -- Python 3.7.3, pytest-6.2.1, py-1.10.0, pluggy-0.13.1 -- /some/path
cachedir: .pytest_cache
rootdir: /some/path
plugins: snapshot-0.4.2, asyncio-0.14.0
collecting ... collected 46 items

tests/configuration/test_configuration_factory.py::test_help PASSED      [  2%]
tests/configuration/test_configuration_factory.py::test_version PASSED   [  4%]
[... many other tests ...]

============================== 46 passed in 0.64s ==============================
Stopping aws-kinesis-consumer_kinesis_1 ... done
Removing aws-kinesis-consumer_kinesis_1 ... done
Removing network aws-kinesis-consumer_default
```

This command will run all the tests on top of a docker container to simulate an AWS Kinesis Stream (
see `docker-compose.yml`).

## Demo: produce and consume mock records

In order to see how the application behaves, the `demo` command can help to produce dummy records, and also to
run `aws-kinesis-consumer` to consume those dummy records from a mocked AWS Kinesis Stream running in a docker
container.

```shell
# first start the producer...
pipenv run invoke demo produce
```

In another terminal, run the following command to start consuming by using the source code of `aws-kinesis-consumer` :

```shell
# ...then start the consumer
pipenv run invoke demo consume
```

## Other commands

All the following commands can be triggered using `pipenv run invoke <COMMAND>`. See
the [invoke](https://www.pyinvoke.org/) project.

| Command | Description |
| ------- | ----------- |
| `build` | Builds the application to all supported packages (e.g. pip, Docker). |
| `deploy` | Deploys the previously built packages to PyPi and DockerHub. This is usually done from [Travis CI](https://travis-ci.com/github/thinow/aws-kinesis-consumer). |
| `assertnotodos` | Verifies if there is any missing todos in the code, otherwise fails the build in [Travis CI](https://travis-ci.com/github/thinow/aws-kinesis-consumer). |
| `snapshots` | Updates the Pytest snapshots (see [pytest-snapshot](https://pypi.org/project/pytest-snapshot/)). |
