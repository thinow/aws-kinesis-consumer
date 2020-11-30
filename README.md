# aws-kinesis-consumer

**aws-kinesis-consumer** offers the ability to simply look up the records from a AWS Kinesis Data Stream.

## Motivation

The [AWS CLI](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/kinesis/index.html) is able to fetch
records from Kinesis, but the users need to list the shards, to generate iterator tokens, use subsequent tokens, delay
operations, and so on.

aws-kinesis-consumers in contrary is able to get records from the stream name only. So users can simply scrap a stream
to watch some records without any extra script.
