[![PyPI version](https://img.shields.io/pypi/v/aws-kinesis-consumer.svg)](https://pypi.org/project/aws-kinesis-consumer)
[![Python versions](https://img.shields.io/pypi/pyversions/aws-kinesis-consumer.svg)](https://pypi.org/project/aws-kinesis-consumer)
[![Docker version](https://img.shields.io/docker/v/thinow/aws-kinesis-consumer?sort=semver&label=docker)](https://hub.docker.com/r/thinow/aws-kinesis-consumer)
[![Build Status](https://travis-ci.com/thinow/aws-kinesis-consumer.svg?token=vwaCq8jYcvaxfHBRGUqa&branch=master)](https://travis-ci.com/thinow/aws-kinesis-consumer)

# aws-kinesis-consumer

Consume an [AWS Kinesis Data Stream](https://aws.amazon.com/kinesis/data-streams/) to look over the records from a terminal.

## Demo

```shell
$ aws-kinesis-consumer --stream-name MyStream
> preparing shards 2/2
> shard_id=shardId-000000000000, records=1
Record-001
> shard_id=shardId-000000000001, records=2
Record-002
Record-003
```

## Usage

### Pre-requirement

Connect to AWS and set
the [default AWS environment variables](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-envvars.html#envvars-list)
.

```shell script
export AWS_DEFAULT_REGION=eu-central-1
export AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
export AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
```

Alternatively, [aws configure](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html#cli-configure-files-methods)
can help to set the environment variables.

### Use with Python

```shell
# install
pip install aws-kinesis-consumer

# consume a stream
aws-kinesis-consumer --stream-name MyStream
```

### Use with Docker

```shell
docker run \
  -e AWS_DEFAULT_REGION \
  -e AWS_ACCESS_KEY_ID \
  -e AWS_SECRET_ACCESS_KEY \
  -e AWS_SESSION_TOKEN \
  thinow/aws-kinesis-consumer --stream-name MyStream
```

### Arguments

|      |     | Default | Description |
| ---- | --- | ------- | ----------- |
| `-s` | `--stream-name` |  | **REQUIRED** Name of the AWS Kinesis Stream. |
| `-e` | `--endpoint` |  | Custom AWS endpoint url to communicate with the AWS API. Could be used in order to specify a region (e.g. `https://kinesis.us-east-1.amazonaws.com/`). |
| `-i` | `--iterator-type` | `latest` | Defines how to start consuming records from the stream. Use `latest` to consume the new records only. Or use `trim-horizon` to consume all the records already existing in the stream. |
| `-m` | `--max-records-per-request` | `10` | Defines the maximum number of records per request. |
| `-r` | `--region` |  | AWS region of the stream (e.g. `us-east-1`). By default, the AWS region available in your terminal (e.g. environment variable `AWS_DEFAULT_REGION`). |
|<img width="130"/>|<img width="400"/>|<img width="0"/>|<img width="0"/>|
| `-h` | `--help` |  | Prints the help message. |
| `-V` | `--verbose` |  | Prints all the details when an error stops the application. |
| `-v` | `--version` |  | Prints the version of the binary. |

## FAQ

### What is the motivation ? What is the issue with AWS CLI ?

The [AWS CLI](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/kinesis/index.html) is able to fetch
records from Kinesis, but the users need to list the shards, to generate iterator tokens, use subsequent tokens, delay
operations, and so on.

`aws-kinesis-consumer` in contrary is able to get records by using the stream name, and only the stream name. Therefore
there is no need for an extra script.

### How to filter the records ?

`aws-kinesis-consumer` can be piped with other command such as [grep](https://www.man7.org/linux/man-pages/man1/grep.1.html),
or even [jq](https://stedolan.github.io/jq/) to filter json records.

```shell
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
$ aws-kinesis-consumer --stream-name MyStream | jq 'select(.status == "error")'
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

### How to contribute to the project ?

[See the guidelines in the CONTRIBUTING.md file](https://github.com/thinow/aws-kinesis-consumer/blob/master/CONTRIBUTING.md)
.

## Changelog

[See all the changes per release](https://github.com/thinow/aws-kinesis-consumer/blob/master/CHANGELOG.md).

## Special thanks

* Thanks to the contributors of the [kinesalite](https://github.com/mhart/kinesalite) project which make test and
  development of this project extremely easy and reliable!
