import uuid

import boto3
from boto3_type_annotations.kinesis import Client as Kinesis


class MockedKinesis:
    endpoint: str
    kinesis: Kinesis

    def __init__(self, endpoint: str) -> None:
        self.endpoint = endpoint
        self.kinesis = boto3.client('kinesis', endpoint_url=endpoint)

    def create_mocked_stream(self):
        stream_name = f'mocked-stream-{uuid.uuid4()}'
        self.kinesis.create_stream(
            StreamName=stream_name,
            ShardCount=1
        )
        return MockedStream(self.kinesis, stream_name)


class MockedStream:
    def __init__(self, kinesis: Kinesis, name: str) -> None:
        self.kinesis = kinesis
        self.name = name

    def put_record(self, data: str):
        self.kinesis.put_record(
            StreamName=self.name,
            PartitionKey=str(uuid.uuid4()),
            Data=data.encode(),
        )
