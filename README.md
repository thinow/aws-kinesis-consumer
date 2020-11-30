[![PyPI version](https://img.shields.io/pypi/v/aws-kinesis-consumer.svg)](https://pypi.org/project/aws-kinesis-consumer)
[![Python versions](https://img.shields.io/pypi/pyversions/aws-kinesis-consumer.svg)](https://pypi.org/project/aws-kinesis-consumer)
[![Build Status](https://travis-ci.com/thinow/aws-kinesis-consumer.svg?token=vwaCq8jYcvaxfHBRGUqa&branch=master)](https://travis-ci.com/thinow/aws-kinesis-consumer)

# aws-kinesis-consumer

**aws-kinesis-consumer** offers the ability to simply look up the records from a AWS Kinesis Data Stream.

## Motivation

The [AWS CLI](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/kinesis/index.html) is able to fetch
records from Kinesis, but the users need to list the shards, to generate iterator tokens, use subsequent tokens, delay
operations, and so on.

aws-kinesis-consumers in contrary is able to get records from the stream name only. So users can simply scrap a stream
to watch some records without any extra script.
