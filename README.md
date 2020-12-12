[![PyPI version](https://img.shields.io/pypi/v/aws-kinesis-consumer.svg)](https://pypi.org/project/aws-kinesis-consumer)
[![Build Status](https://travis-ci.com/thinow/aws-kinesis-consumer.svg?token=vwaCq8jYcvaxfHBRGUqa&branch=master)](https://travis-ci.com/thinow/aws-kinesis-consumer)

# aws-kinesis-consumer

Consume an [AWS Kinesis Data Stream](https://aws.amazon.com/kinesis/data-streams/) to look over the records from a terminal.

## Demo

```shell script
$ aws-kinesis-consumer --stream-name MyStream

Record-001
Record-002
Record-003
```

## Install

[Python 3.6+](https://www.python.org/downloads/) needs to be already installed, then :

```shell script
pip install aws-kinesis-consumer
```

## Usage

Just as the [AWS CLI](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/kinesis/index.html),
``aws-kinesis-consumer`` will use the AWS credentials pre-configured on the machine. Here are more details to [setup AWS
credentials](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html).

### Consume a stream

```shell script
aws-kinesis-consumer --stream-name MyStream
```

### Define position of the expected messages in the stream

```shell script
# Consume only the new messages
aws-kinesis-consumer --stream-name MyStream --iterator-type latest

# Consume the messages already produced in the stream 
aws-kinesis-consumer --stream-name MyStream --iterator-type trim-horizon
```

### Consume a stream hosted in a different region

```shell script
AWS_DEFAULT_REGION=eu-central-1 aws-kinesis-consumer --stream-name MyGermanStream
```

### Define endpoint different from the default AWS service endpoint

```shell script
# Consuming from a different AWS endpoint url
aws-kinesis-consumer --stream-name MyStream --endpoint https://another.kinesis.us-east-1.amazonaws.com/


# Testing a local Kinesis Stream server
aws-kinesis-consumer --stream-name MyStream --endpoint http://localhost:4567/
```

### Display help

```shell script
aws-kinesis-consumer --help
```

## FAQ

### Why not using AWS CLI to consume an AWS Kinesis Stream ?

The [AWS CLI](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/kinesis/index.html) is able to fetch
records from Kinesis, but the users need to list the shards, to generate iterator tokens, use subsequent tokens, delay
operations, and so on.

``aws-kinesis-consumers`` in contrary is able to get records by using the stream name, and only the stream name.
Therefore there is no need for an extra script.

## Special thanks

* Thanks to the contributors of the [kinesalite](https://github.com/mhart/kinesalite) project which make test and development of this project extremely easy and reliable!
