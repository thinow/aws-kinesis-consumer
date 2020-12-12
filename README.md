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

| Argument | Default | Description |
| -------- | ------- | ----------- |
| `--stream-name` _(required)_ | | Name of the AWS Kinesis Stream. |
| `--iterator-type` | `latest` | Defines how to start consuming records from the stream. Use `latest` to consume the new records only. Or use `trim-horizon` to consume all the records already existing in the stream. |
| `--endpoint` |  | Custom AWS endpoint url to communicate with the AWS API. Could be used in order to specify a region (e.g. `https://kinesis.us-east-1.amazonaws.com/`). |
| `--help` | | Shows the help message. | 

## FAQ

### What is the motivation ? What is the issue with AWS CLI ?

The [AWS CLI](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/kinesis/index.html) is able to fetch
records from Kinesis, but the users need to list the shards, to generate iterator tokens, use subsequent tokens, delay
operations, and so on.

``aws-kinesis-consumers`` in contrary is able to get records by using the stream name, and only the stream name.
Therefore there is no need for an extra script.

### How to consume a stream hosted in different regions ?

The environment variable `AWS_DEFAULT_REGION` can be used to specify any AWS region.

```shell script
AWS_DEFAULT_REGION=eu-central-1 aws-kinesis-consumer --stream-name MyGermanStream
```

### How to filter the records ?

`aws-kinesis-consumer` can be piped with other command such as [grep](https://www.man7.org/linux/man-pages/man1/grep.1.html),
or even [jq](https://stedolan.github.io/jq/) to filter json records.

```shell script
# all the records
$ aws-kinesis-consumer --stream-name MyStream
{"name":"foo", "status":"ok"}
{"name":"bar", "status":"pending"}
{"name":"baz", "status":"error"}

# records containing the text "ba" (e.g. "bar" and "baz", but not "foo")
$ aws-kinesis-consumer --stream-name MyStream | grep "ba"
{"name":"bar", "status":"pending"}
{"name":"baz", "status":"error"}

# records where the json property "status" has the value "error"
$ aws-kinesis-consumer --stream-name MyStream | jq 'contains({status:"error"})'
{"name":"baz", "status":"error"}
```

### What are the required AWS permissions ?

`aws-kinesis-consumer` requires the following AWS permissions :
* [kinesis:ListShards](https://docs.aws.amazon.com/kinesis/latest/APIReference/API_ListShards.html)
* [kinesis:GetShardIterator](https://docs.aws.amazon.com/kinesis/latest/APIReference/API_GetShardIterator.html)
* [kinesis:GetRecords](https://docs.aws.amazon.com/kinesis/latest/APIReference/API_GetRecords.html)

The following policy is an example which can be applied to an AWS user or an AWS role :

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "kinesis:ListShards",
                "kinesis:GetShardIterator",
                "kinesis:GetRecords"
            ],
            "Resource": [
                "arn:aws:kinesis:REGION:ACCOUNT-ID:stream/STREAM-NAME"
            ]
        }
    ]
}
```

## Special thanks

* Thanks to the contributors of the [kinesalite](https://github.com/mhart/kinesalite) project which make test and development of this project extremely easy and reliable!
