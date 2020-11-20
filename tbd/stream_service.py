import boto3
from boto3_type_annotations.kinesis import Client as KinesisClient


class StreamService:
    kinesis: KinesisClient

    def __init__(self) -> None:
        self.kinesis = boto3.client('kinesis')

    def get_names_of_streams(self) -> list:
        response = self.kinesis.list_streams()
        return response['StreamNames']
