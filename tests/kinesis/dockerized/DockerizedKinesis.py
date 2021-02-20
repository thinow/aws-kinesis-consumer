import uuid

import boto3
from boto3_type_annotations.kinesis import Client as Kinesis

DUMMY_AWS_ENV_VARS = {
    "AWS_ACCESS_KEY_ID": "anything",
    "AWS_SECRET_ACCESS_KEY": "anything",
}


class DockerizedKinesis:
    region: str
    endpoint: str
    kinesis: Kinesis

    def __init__(self, endpoint: str) -> None:
        self.region = 'anything'
        self.endpoint = endpoint
        self.kinesis = boto3.client('kinesis', endpoint_url=endpoint, region_name=self.region)

    def create_dockerized_stream(self):
        stream_name = f'dockerized-stream-{uuid.uuid4()}'
        self.kinesis.create_stream(
            StreamName=stream_name,
            ShardCount=1
        )
        return DockerizedStream(self.kinesis, stream_name)


class DockerizedStream:
    def __init__(self, kinesis: Kinesis, name: str) -> None:
        self.kinesis = kinesis
        self.name = name

    def put_record(self, data: str):
        self.kinesis.put_record(
            StreamName=self.name,
            PartitionKey=str(uuid.uuid4()),
            Data=data.encode(),
        )

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.kinesis.delete_stream(
            StreamName=self.name,
        )
